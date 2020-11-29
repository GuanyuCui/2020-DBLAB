from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib import auth
from django.contrib.auth.decorators import login_required

import json
from apps import myforms
from apps import models


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
    
def handle_uploaded_file(f,filename):
    with open('data/%s' % filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def download(request):
    file = open('data/4.2011-Personalized News Recommendation A Review and an Experimental Investigation.pdf', 'rb')
    response = HttpResponse(file)

    #设置头信息，告诉浏览器这是个文件
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="a.pdf"'

    return response

def insert_process(request):
    # print("why?")
    # print(request)
    if request.method == 'POST':
        # 可以设定重定向的url
        back_dic = {'url':'','code':1000}
        
        data = request.POST

        title = data['title']
        language = data['language']
        cj = data['cj']
        cjname = data['cjname']
        cjtype = data['cjtype']
        date = data['date']
        page_1 = data['page_1']
        page_2 = data['page_2']

        # 会议没有卷期
        try:
            volume = data['volume']
            issue = data['issue']
        except:
            pass

        authors = data['authors']
        authors = json.loads(authors)
        
        # print(authors,type(authors[0]))


        # 存储pdf文件, 默认在data/paper.pdf
        paper = request.FILES['paper']
        paper_name = request.FILES['paper'].name
        handle_uploaded_file(paper,paper_name)

        return JsonResponse(back_dic)
        
    else:
        return HttpResponse("<h1>WRONG!</h1>")

def query_process(request):
    if request.method == 'POST':
        back_dic = {'url':'','code':1000}
        data = request.POST
        # 数据形式可以在query页的console中查看
        print(data,type(data))
        return JsonResponse(back_dic)

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

# 添加
@login_required
def insert(request):
    return render(request, 'insert.html', locals())

# 查询
@login_required
def query(request):
    return render(request, 'query.html', locals())

# 详细信息
@login_required
def detail(request, paperid):
    # paperid这里后面要改，目前暂时同title代替！！！
    paper = models.Paper.objects.raw('SELECT * FROM Paper WHERE title=%s;', [paperid])[0]
    # print([str(paper.conferjournalname)])
    conferjournal = models.Conferjournal.objects.raw('SELECT * FROM Conferjournal WHERE name=%s;', [str(paper.conferjournalname)])[0]
    authors = models.Pa.objects.filter(papertitle=str(paper.title))
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

    # 送到前端显示

    # 再送回后端

    return render(request, 'modify.html', locals())

# 主页
@login_required
def home(request):
    # 如果是管理员，则返回所有待审核的项目
    if request.user.is_staff:
        print(1)
        # 等临时表建好了再说
    else:
        print(request.user.username)
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

    img_obj = Image.new('RGB', (310, 35), get_random_rgb())
    img_draw = ImageDraw.Draw(img_obj)  # 生成一个画笔对象
    img_font = ImageFont.truetype('static/font/111.ttf', 30)  # 字体的样式
    """
    所有的字体样式都是由.ttf结尾的文件控制的
    """
    # 随机生成验证码  a~z  A~Z  0~9
    code = ''
    for i in range(5):
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
