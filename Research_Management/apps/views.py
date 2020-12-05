from os import name
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.db.models import Q

# deprecated
# from apps.myforms import ExportForm
import re
import bibtexparser as bp
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

import json
import csv
from apps import myforms
from apps import models
from apps.models import Paper
from apps.models import Author
from apps.models import Conferjournal
from apps.models import Pa
from apps.models import Tmppaper
from apps.models import Tmppa

# 这个别删
rank_refer = ['A+','A','A-','B','C']
papertype_refer = ['正刊','专刊','增刊','长文Oral','长文Poster','短文Oral','短文Poster','Demo']
authoridentity_refer = ['第一作者','通讯作者','其他作者']
export_refer = ['论文题目','发表刊物简称','发表刊物全称','刊物在学校的等级','刊物在CCF的等级','刊物类型','发表时间','全部作者名字','第一作者姓名','第一作者类型','通讯作者姓名','通讯作者类型','论文页码起止范围','卷','期','正刊还是增刊','举办国家','举办城市','长文/短文/demo','oral/poster']

condition_refer = {'AND':'&','OR':'|','':''}
key_refer = {'期刊/会议名称':'conferjournalname__name','论文题目':'title','作者姓名':'pa__authorname'}
confer_journal_refer = {'C':'会议','J':'期刊'}
papertype_detail_refer = {'长文Oral':'长文','长文Poster':'长文','短文Oral':'短文','短文Poster':'短文','Demo':'Demo'}
papertype_repr_refer = {'长文Oral':'Oral','长文Poster':'Poster','短文Oral':'Oral','短文Poster':'Poster'}

# 设置用户权限的一篇参考博文
# https://www.cnblogs.com/xuchengcheng1215/p/9457950.html
# 由于后期需要做出普通用户与管理员的区分

# 测试函数
def test(request):

    if request.user.is_staff:
        print('is staff')

    return render(request, 'base.html')

# 注册
# todo：只有管理员可以注册，因此后期还得加一个if判断
@login_required
def createuser(request):
    # 判断是否是管理员
    if not request.user.is_staff:
        return
    # 产生一个空对象
    form_obj = myforms.MyRegForm()
    if request.method == 'POST':
        back_dic = {'code':1000, 'msg':''}
        # 校验数据
        form_obj = myforms.MyRegForm(request.POST)
        if form_obj.is_valid():
            # form_obj.cleaned_data  # {'username':'','password':'','confirm_password':'','email':''}
            clean_data = form_obj.cleaned_data
            clean_data.pop('confirm_password')  #  {'username':'','password':'','email':''}
            models.UserInfo.objects.create_user(**clean_data)
            # 目前想法是注册完之后弹出注册完成的框，不跳转
            # back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'createuser.html', locals())

# def update_password(request):

@login_required
def set_password(request):
    if request.is_ajax():
        back_dic = {'code':1000,'msg':''}
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # 新密码长度正确
            if len(new_password) >=3 and len(new_password) <= 8:
                # 两次密码一致
                if new_password == confirm_password:
                    is_right = request.user.check_password(old_password)
                    # 原密码正确
                    if is_right:
                        request.user.set_password(new_password)
                        request.user.save()
                        back_dic['url'] = '/index/'
                    # 原密码不正确
                    else:
                        back_dic['code'] = 3000
                        back_dic['msg'] = '原密码错误'
                # 两次密码不一致
                else:
                    back_dic['code'] = 2000
                    back_dic['msg'] = '两次密码不一致'
            # 新密码长度不正确
            else:
                back_dic['code'] = 2000
                if len(new_password) < 3:
                    back_dic['msg'] = '新密码长度不能少于三位'
                else:
                    back_dic['msg'] = '新密码长度不能多于八位'
            return JsonResponse(back_dic)    

def handle_uploaded_file(f,filename):
    with open('data/%s' % filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def download(request,paperid):
    file = open('data/{}.pdf'.format(paperid), 'rb')
    response = HttpResponse(file)

    #设置头信息，告诉浏览器这是个文件
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=\"{}.pdf\"'.format(paperid)

    return response

def export(request, paperids):
    # if request.method == 'POST':
        # export_form = ExportForm(request.POST)
        # if export_form.is_valid():
            # export_list = json.loads(export_form.cleaned_data['paperids'])
    if paperids:
        export_list = json.loads(paperids)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="output.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response,dialect='excel')
        writer.writerow(export_refer)

        for paperid in export_list:
            paper = Paper.objects.get(paperid=paperid)
            authors = Pa.objects.filter(paperid=paperid).order_by("authorrank")
            authors_str = ';'.join([i.authorname for i in authors])
            author_frst = authors.get(authorrank=1, authoridentity='普通作者')
            try:
                author_tele = authors.get(authoridentity="通讯作者")
                author_tele_name = author_tele.authorname
                author_tele_type = author_tele.authortype
            except:
                author_tele_name = ''
                author_tele_type = ''
            page_span = str(paper.startpage) + '~' + str(paper.endpage)

            if paper.conferorjournal == 'C':
                writer.writerow([
                    paper.title, paper.conferjournalname.abbreviation, paper.conferjournalname,
                    paper.conferjournalname.ruclevel, paper.conferjournalname.ccflevel, confer_journal_refer[paper.conferorjournal],
                    paper.publishtime.strftime("%Y-%m-%d"), authors_str, author_frst.authorname, author_frst.authortype,
                    author_tele_name, author_tele_type, 
                    page_span, '', '', '', paper.conferencecountry, paper.conferencecity, papertype_detail_refer[paper.papertype],
                    papertype_repr_refer[paper.papertype]
                ])
            elif paper.conferorjournal == 'J':
                writer.writerow([
                    paper.title, paper.conferjournalname.abbreviation, paper.conferjournalname,
                    paper.conferjournalname.ruclevel, paper.conferjournalname.ccflevel, confer_journal_refer[paper.conferorjournal],
                    paper.publishtime.strftime("%Y-%m-%d"), authors_str, author_frst.authorname, author_frst.authortype,
                    author_tele_name, author_tele_type, 
                    page_span, paper.volume, paper.issue, paper.papertype, '', '', ''
                ])
        return response 
    else:
        return render(request, 'errors.html')

def api_dropbox(request):
    """
        相应下拉框的查询
    """
    if request.method == 'POST':
        query = request.POST
        if query.field == 'authorname':
            results = Author.objects.filter(name=query.term)
            results = json.dumps([{'id':index, 'authorname':result.name} for index,result in enumerate(results)])
        if query.field == 'conferjournal':
            results = Conferjournal.objects.filter(name)


def query_process(request):
    """ 处理query

        完成的: 
            可以解析手动输入的query和勾选框的内容, 都在print里有输出
        TODO: 
            filter(a,b) 和 filter(a).filter(b)的逻辑
    """
    if request.method == 'POST':
        data = request.POST
        
        if "is_first" in data:
            back_dic = {'draw': 1, 'recordsTotal': 0, 'data': '[]'}
            return JsonResponse(back_dic)

        queries =json.loads(data['queries'])
        authorIdentity = json.loads(data['authorIdentity'])
        paperType = json.loads(data['paperType'])
        CCFRank = json.loads(data['CCFRank'])
        CCFChinaRank = json.loads(data['CCFChinaRank'])
        RUCRank = json.loads(data['RUCRank'])
        time = json.loads(data['time'])

        # conferorjournal = paperType[0] and paperType[1] and paperType[2]
        
        results = Paper.objects
        
        if request.user.is_staff:

            # # a or b and c = a or (b and c)
            # if queries[0]['value']:
            #     query_str = ''
            #     for idx,query in enumerate(queries):
            #         condition = condition_refer[query['condition']]
            #         key = key_refer[query['key']]
            #         value = query['value']

            #         query_str += (condition + "Q({}=\"{}\")".format(key,value))
                
            #     query_str = "results.objects.filter({})".format(query_str)
            #     results = eval(query_str)
            #     print("results after top queries:{}".format(results))

            # 这是使用交集并集的逻辑, 也就是遇到 a or b and c 即执行 (a or b) and c
            # 查询时需要distinct()否则会重复, 注意使用distinct()之后的order_by不能设计别的数据表中的列
            if queries[0]['value']:
                for idx,query in enumerate(queries):
                    condition = query['condition']
                    key = key_refer[query['key']]
                    value = query['value']

                    # 获取第一个条件
                    if idx == 0:
                        if key == 'pa__authorname':
                                result = eval("Paper.objects.filter({}=\"{}\").distinct()".format(key,value))
                        else:
                            result = eval("Paper.objects.filter({}__contains=\"{}\").distinct()".format(key,value))
                        results = result

                    # 如果还有别的条件
                    else:
                        if not value:
                            continue

                        # and做交
                        if condition == 'AND':
                            if key == 'pa__authorname':
                                result = eval("Paper.objects.filter({}=\"{}\").distinct()".format(key,value))
                            else:
                                result = eval("Paper.objects.filter({}__contains=\"{}\").distinct()".format(key,value))
                            results = results&result

                        # or做并
                        if condition == 'OR':
                            if key == 'pa__authorname':
                                result = eval("Paper.objects.filter({}=\"{}\").distinct()".format(key,value))
                            else:
                                result = eval("Paper.objects.filter({}__contains=\"{}\").distinct()".format(key,value))                            
                            results = (results|result).distinct()

                print("results after top queries:{}".format(results))
                    
        else:
            user = Author.objects.get(authorid=request.user.username)
            results_ = results.filter(pa__authorname=user.name)
            print("current user:{}, user name:{}, results after name query:{}".format(user,user.name,results))
            
            if queries[0]['value']:
                for idx,query in enumerate(queries):
                    condition = query['condition']
                    key = key_refer[query['key']]
                    value = query['value']

                    # 获取第一个条件
                    if idx == 0:
                        result = eval("results_.objects.filter({}=\"{}\").distinct()".format(key,value))
                        results = result

                    # 如果还有别的条件
                    else:
                        if not value:
                            continue
                        # and做交
                        if condition == 'AND':
                            result = eval("results_.objects.filter({}=\"{}\").distinct()".format(key,value))
                            results = results&result

                        # or做并
                        if condition == 'OR':
                            result = eval("results_.objects.filter({}=\"{}\").distinct()".format(key,value))
                            results = (results|result).distinct()
                
                print("results after top queries:{}".format(results))

            else:
                results = results_

        # 如果查到一半就变空集, 那就不用继续查
        if results:
            # 处理日期的query时, 用户可以只填写一边的日期
            # time queries:
            q_time = []
            if time[0]:
                q_time.append("Q(publishtime__gte=\"%s\")" % time[0])
            if time[1]:    
                q_time.append("Q(publishtime__lte=\"%s\")" % time[1])
            
            time_query = '&'.join(q_time)
            time_query_str = "results.filter({})".format(time_query)
            results = eval(time_query_str)
            print("results after time queries:{}".format(results))

        if results:    
            q_ai = []
            if authorIdentity[0]:
                q_ai.append("Q(pa__authoridentity=\"普通作者\",pa__authorrank=1)")
            if authorIdentity[1]:
                q_ai.append("Q(pa__authoridentity=\"通讯作者\")")
            if authorIdentity[2]:
                q_ai.append("Q(pa__authoridentity=\"普通作者\",pa__authorrank__gt=1)")
            
            authoridentity_query = '|'.join(q_ai)
            print(Paper.objects.filter(pa__authoridentity="普通作者").filter(pa__authoridentity="通讯作者"))
            authoridentity_query_str = "results.filter({}).distinct()".format(authoridentity_query)
            results = eval(authoridentity_query_str)
            print("results after author identity queries:{}".format(results))

        if results:
            # 0: main, 1: special section, 2: addition
            # 3: long oral, 4: long poster, 5: short oral, 6: short poster
            # 7: demo
            # paper type queries:
            q_pt = []
            for idx in range(8):
                if paperType[idx] == 1:
                    papertype = papertype_refer[idx]
                    q_pt.append("Q(papertype=\"%s\")" % papertype)
            
            papertype_query = '|'.join(q_pt)
            papertype_query_str = "results.filter({})".format(papertype_query)
            results = eval(papertype_query_str)
            print("results after paper type queries:{}".format(results))

        if results:
            # rank queries
            q_ccf = []
            q_ccfchina = []
            q_ruc = []
            for idx in range(5):
                if CCFRank[idx] == 1:
                    rank = rank_refer[idx]
                    q_ccf.append("Q(conferjournalname__ccflevel=\"%s\")" % rank)

                if CCFChinaRank[idx] == 1:
                    rank = rank_refer[idx]
                    q_ccfchina.append("Q(conferjournalname__ccfchinalevel=\"%s\")" % rank)

                if RUCRank[idx] == 1:
                    rank = rank_refer[idx]
                    q_ruc.append("Q(conferjournalname__ruclevel=\"%s\")" % rank)

            rank_query = '|'.join(q_ccf + q_ccfchina + q_ruc)
            rank_query_str = "results.filter({})".format(rank_query)
            results = eval(rank_query_str)
            print("results after rank quries:{}".format(results))

        if results:
            back_dic = {'draw':1, "recordsTotal": len(results)}
            # results = results.values('paperid','title','conferjournalname','publishtime')
            results = json.dumps([{'paperid':i.paperid,'title':i.title,'conferjournalname':i.conferjournalname.name,'publishtime':str(i.publishtime)} for i in (results)])
            back_dic['data'] = results
        else:
            back_dic = {'draw':1, 'recordsTotal': 0, 'error': '无搜索结果！', 'data': '[]'}
        # print(back_dic)
        return JsonResponse(back_dic)
    else:
        render(request,'erros.html')

def errors(request):
    return render(request, 'errors.html', locals())
    
# 首页
def index(request):
    # 如果用户已登录，则跳转到主页
    if request.user.is_authenticated:
        return redirect('/home/')
    # 用户登录模块
    if request.method == 'POST':
        back_dic = {'code':1000, 'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1 先校验验证码是否正确
        if request.session.get('code').upper() == code.upper():
            # 2 校验用户名和密码是否正确
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 3 保存用户登录状态
                auth.login(request, user_obj)
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)

    return render(request, 'index.html')

# 登录
def login(request):
    if request.method == 'POST':
        back_dic = {'code':1000, 'msg':''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        # 1 先校验验证码是否正确
        if request.session.get('code').upper() == code.upper():
            # 2 校验用户名和密码是否正确
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 3 保存用户登录状态
                auth.login(request, user_obj)
                back_dic['url'] = '/home/'
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic)
    return render(request, 'login.html')

# 登出
@login_required
def logout(request):
    # 删除用户session信息
    auth.logout(request)  # request.session.flush()
    return redirect('/index/')

def bibtex(request):
    if request.method == 'POST':
        # 可以设定重定向的url
        back_dic = {'url':'/home/','code':1000}
        data = request.POST
        bibfile = data['bibtex']
        print(bibfile)
        parser = BibTexParser()  # 声明解析器类
        parser.customization = convert_to_unicode  # 将BibTeX编码强制转换为UTF编码
        bibdata = bp.load(bibfile, parser = parser)  # 通过bp.load()加载

        volume = bibdata.entries[0]['volume']
        issue = bibdata.entries[0]['number']
        title = bibdata.entries[0]['title'].replace("\n", " ")
        pages = bibdata.entries[0]['pages']
        matchObj = re.match( r'(.*)--(.*)', pages, re.M|re.I)
        if matchObj:
            print ("matchObj.group(1) : ", matchObj.group(1))
            print ("matchObj.group(2) : ", matchObj.group(2))
            startpage = matchObj.group(1)
            endpage = matchObj.group(2)
        else:
            print ("No match!!")

        biburl = bibdata.entries[0]['biburl']
        print(biburl)
        matchObj2 = re.match( r'(.*)rec/(.*)/(.*)/(.*)', biburl, re.M|re.I)
        if matchObj:
            print ("matchObj.group(2) : ", matchObj2.group(2))
            print ("matchObj.group(2) : ", matchObj2.group(3))
            CorJ = matchObj2.group(2)
            conferjournalabb = matchObj2.group(3)
            cJobj = Conferjournal.objects.filter(pa__abbreviation = conferjournalabb.upper())
            conferjournalname = cJobj.conferjournalname
            if (CorJ == 'journals'):
                conferorjournal = 'J'
            else:
                conferorjournal = 'C'
        else:
            print ("No match in biburl")
            


# 添加
@login_required
def insert(request):
    # print("why?")
    # print(request)
    print('inserting')
    if request.method == 'POST':
        # 可以设定重定向的url
        back_dic = {'url':'/home/','code':1000}
        data = request.POST
        # 判断是否是第一次发送ajax
        if data['is_first'] == '1':
            # 判断是否存在重名项
            is_title_same = models.Paper.objects.filter(title=data['title'])
            if is_title_same:
                back_dic['code'] = 2000
                return JsonResponse(back_dic)

        newPaper = Tmppaper() # 实例化数据表
        commitAuthor_obj = Author.objects.get(authorid = request.user.username)   
        newPaper.commitauthorid = commitAuthor_obj
        newPaper.title = data['title']

        Conferjournal_obj = Conferjournal.objects.get(name = data['cjname'])   
        newPaper.conferjournalname = Conferjournal_obj
        if data['language'] == 'English':
            newPaper.language = 'E'
        else:
            newPaper.language = 'C'
        if data['cj'] == 'journal':
            newPaper.conferorjournal = 'J'
        else:
            newPaper.conferorjournal = 'C'
        newPaper.papertype = data['cjtype']
        newPaper.publishtime = data['date']
        newPaper.startpage = data['page_1']
        newPaper.endpage = data['page_2']
        try:
            newPaper.volume = data['volume']
            newPaper.issue = data['issue']
        except:
            pass
        newPaper.save()
        ############# insert into tmpPA #######
        authors = data['authors']
        authors = json.loads(authors)
        for i in range(len(authors)):
            newTmppa = Tmppa()
            newTmppa.paperid = newPaper
            # print(authors[i]['name'])
            newTmppa.authorname = authors[i]['name']
            newTmppa.authorrank = i+1
            newTmppa.authoridentity = authors[i]['identity']
            newTmppa.authortype = authors[i]['type']
            newTmppa.save()
            #newTmppa.authortype = authors[i]['type']
        
        # 存储pdf文件, 默认在data/paper.pdf
        paper = request.FILES['paper']
        paper_name = request.FILES['paper'].name
        handle_uploaded_file(paper,paper_name)
        print("insert successfully!")
        return JsonResponse(back_dic)
    #else:
        #return HttpResponse("<h1>WRONG!</h1>")

    return render(request, 'insert.html', locals())

# 查询
@login_required
def query(request):
    return render(request, 'query.html', locals())

# 详细信息
@login_required
def detail(request, paperid):
    # paperid这里后面要改，目前暂时同title代替！！！
    paper = models.Paper.objects.raw('SELECT * FROM Paper WHERE paperid=%s;', [paperid])[0]
    # print([str(paper.conferjournalname)])
    conferjournal = models.Conferjournal.objects.raw('SELECT * FROM Conferjournal WHERE name=%s;', [str(paper.conferjournalname)])[0]
    authors = models.Pa.objects.filter(paperid=paperid)
    # authors = models.Pa.objects.raw('SELECT Author.name as name, authoridentity,  FROM PA, Author WHERE PA.papertitle=%s AND PA.authorid=Author.authorid', [str(paper.title)])
    # for author in authors:
    #     print(author)
        
    return render(request, 'detail.html', locals())

# 修改内容
@login_required
def modify(request, paperid):
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        return JsonResponse(back_dic)

    # 从临时表查询出来数据
    paper = models.Paper.objects.raw('SELECT * FROM Tmppaper WHERE paperid=%s;', [paperid])[0]
    title = paper.title
    conferorjournal = paper.conferorjournal
    conferjournalname = paper.conferjournalname
    publishtime = paper.publishtime
    volume = paper.volume
    issue = paper.issue
    startpage = paper.startpage
    endpage = paper.endpage
    papertype = paper.papertype
    language = paper.language
    confercountry = paper.conferencecountry
    confercity = paper.conferencecity

    authors = models.Tmppa.objects.filter(paperid = paper.paperid)
    author_names = str([_.authorname for _ in authors]).replace("'", '"')
    author_identities = str([_.authoridentity for _ in authors]).replace("'", '"')
    author_types = str([_.authortype for _ in authors]).replace("'", '"')
    return render(request, 'modify.html', locals())

# 审核
@login_required
def check(request, paperid):#, paperid):
    if request.method == 'POST':
        #back_dic = {'code': 1000, 'msg': ''}

        # 可以设定重定向的url
        back_dic = {'url':'','code':1000}
        data = request.POST
        insertPaper = Paper() # 实例化插入表

        print("username")
        print(request.user.username)  
        #newPaper.commitauthorid = commitAuthor_obj
        insertPaper.title = data['title']

        Conferjournal_obj = Conferjournal.objects.get(name = data['cjname'])   
        insertPaper.conferjournalname = Conferjournal_obj

        if data['language'] == 'English':
            insertPaper.language = 'E'
        else:
            insertPaper.language = 'C'

        if data['cj'] == 'journal':
            insertPaper.conferorjournal = 'J'
    
        else:
            insertPaper.conferorjournal = 'C'

        insertPaper.papertype = data['cjtype']
        insertPaper.publishtime = data['date']
        insertPaper.conferencelocation = data['Conferencelocation']
        insertPaper.startpage = data['page_1']
        insertPaper.endpage = data['page_2']
        # 会议没有卷期
        try:
            insertPaper.Volume = data['volume']
            insertPaper.Issue = data['issue']
        except:
            pass
        insertPaper.save()
        ############# insert into tmpPA #######
        authors = data['authors']
        authors = json.loads(authors)
        # print(authors)
        # print(len(authors))
        # print(authors[0]['name'])

        for i in range(len(authors)):
            newPa = Pa()
            newAuthor = Author()
            newPa.paperid = insertPaper.paperid
            print(authors[i]['name'])
            newPa.authorname = authors[i]['name']
            newPa.authorrank = i+1
            newPa.authoridentity = authors[i]['identity']
            newPa.save()
            #若为校外人员，则插入一条新的Author记录
            try:
                Author_obj = Author.objects.get(name = newPa.authorname)
            except:
                newAuthor.name = newPa.authorname
                newAuthor.authorid = newPa.authorname
                newAuthor.save()
            
            #newPa.authortype = authors[i]['type']
        

        #for i in range(len(authors)):
        #   authorName = authors[i]['name']
        #   authorIdendity = authors[i]['identity']
        #   authorType = authors[i]['type']
        
        # 存储pdf文件, 默认在data/paper.pdf
        paper = request.FILES['paper']
        paper_name = request.FILES['paper'].name
        handle_uploaded_file(paper,paper_name)
        print("save success")
        return JsonResponse(back_dic)
        
    # else:
    #   return HttpResponse("<h1>WRONG!</h1>")
    # 从临时表查询出来数据
    paper = models.Paper.objects.raw('SELECT * FROM Tmppaper WHERE paperid=%s;', [paperid])[0]
    title = paper.title
    conferorjournal = paper.conferorjournal
    conferjournalname = paper.conferjournalname
    publishtime = paper.publishtime
    volume = paper.volume
    issue = paper.issue
    startpage = paper.startpage
    endpage = paper.endpage
    papertype = paper.papertype
    language = paper.language
    confercountry = paper.conferencecountry
    confercity = paper.conferencecity

    authors = models.Tmppa.objects.filter(paperid = paper.paperid)
    author_names = str([_.authorname for _ in authors]).replace("'", '"')
    author_identities = str([_.authoridentity for _ in authors]).replace("'", '"')
    author_types = str([_.authortype for _ in authors]).replace("'", '"')
    return render(request, 'check.html', locals())

# 主页
@login_required
def home(request):
    # 如果是管理员，则返回所有待审核的项目
    if request.user.is_staff:
        # print(1)
        # 等临时表建好了再说
        tmp_papers = models.Tmppaper.objects.all().order_by('paperid')
    else:
        tmp_papers = models.Tmppaper.objects.filter(commitauthorid=request.user.username).order_by('paperid')
        # print(request.user.username)
    return render(request,'home.html', locals())



# 图片验证码相关

from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO


def get_code(request):
    '''生成验证码，在图片上写字'''
    def get_random_rgb():
        '''随机生成RGB颜色'''
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    img_obj = Image.new('RGB', (310, 35), (255, 255, 255))  # white background
    img_draw = ImageDraw.Draw(img_obj)  # 生成一个画笔对象
    img_font = ImageFont.truetype('static/font/111.ttf', 30)  # 字体的样式
    """
    所有的字体样式都是由.ttf结尾的文件控制的
    """
    # 随机生成验证码  a~z  A~Z  0~9
    code = ''
    for i in range(4):
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        random_int = str(random.randint(0, 9))
        temp = random.choice([random_upper, random_lower, random_int])
        # 将产生的随机字符写到图片上
        img_draw.text((i*45+45,0), temp, get_random_rgb(), img_font)
        code += temp
    print(code)
    # 将随机验证码存储取来  以便其他函数调用
    request.session['code'] = code

    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


@login_required
def delete_tmp_paper(request):
    if request.method == 'POST':
        back_dic = {'code':1000}
        data = request.POST
        paperid = data['tmppaperid']
        print(data)
        # 查询该条记录是否存在
        tmp_papers = models.Tmppaper.objects.filter(paperid=paperid)
        #  若该条记录存在，则删除
        if tmp_papers:
            tmp_papers.delete()
        # 若不存在，返回错误代码2000
        else:
            back_dic['code'] = 2000
    return JsonResponse(back_dic)