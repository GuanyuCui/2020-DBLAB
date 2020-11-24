## 后端

*last update：2020.11.13*

### 已实现

**页面部分**

- home

- createuser
  - 以管理员登录时可以自行创建用户

- login
  - *默认管理员为admin，密码也是admin*

- logout
  - 登出后回到登入页
  - 如果没有登录, 则不能访问`insert/`等url

- detail
  - 在数据库中查询后返回前端
  - 具体数据格式问snl

**API部分**

- 获取验证码
- 上传论文pdf, 目前只是功能级别实现, 等到逻辑理顺后再加到页面上
  - 访问`http://127.0.0.1:8000/paper/`, 上传`.pdf`文件后点击上传按钮
  - 在`/Research_Management/data/`下可以看到`paper.pdf`, 就是刚刚上传的论文

**TODO**

1. 解析前端传回来的字典, 将其存入数据库
2. 使用`user/group`细致区分管理员与普通用户的功能区别
3. 修改密码
4. 添加页面，将数据插入临时表
5. 查询也根据query返回相应的数据内容
6. detail页面需要根据paperid来返回数据
7. 主页需要从临时表取数据

## 前端

**TODO**

1.  最好能做一个index页面，然后把login.html和其整合在一起，就像obe一样，现在的login有点丑，以后的逻辑我设想的是一进来就是一个index页，然后登入进入home
2.  css不要写在标签里, 独立出来放到 block css
3.  script，js不要二次引入，base里已经引入了，除非是不用base的页面，但这样的页面引入也要通过本地静态方式引入
4.  详情页面的会议等级是要哪个等级？
5. `insert`页面,
   - 用`ajax`/`javascript` 创建一个`字典(JSON)`, 其中每一个键值对都是输入的值, 用`POST`方法发送到`/process`(这个url是暂时的, 只是方便前端写, 之后由后端统一逻辑后再修改)。

   - 我在`insert.html`最下面写了一段测试的, 还改了`insert`的提交按钮, 你们可以删掉 
6. `query`页面
   - 同理, 把用户填进去的数据**解析成字典(JSON)**, 告诉后端**解析的规则**, 然后用`POST`方法发送到`/process`


**返回数据的例子:**
```python
data_post = {
    "title":"Personalized News Recommendation with Context Trees",
    "papertypeid":"1",
     ...
}
```

## 数据库

1. 添加页面的临时表，作者就全用字符串存，加分隔符
2. 建议将papertype.typeid与paper.papertypeid改为paperid
3. paper中某些二值变量字段需要统一，到底是存一个01变量，还是存它的全称
4. 建议将paper中的location放入conferencejournal表；还有就是paper里加入了会议和期刊，那么为什么存期刊的地方还需要这个属性，建议只保留会议期刊表里的这个属性 **会议每年地点都变**
5. PA中的paid干啥的
6. PA中根本没有存作者的类型，这个属性是不是不太需要（建议再问问老师）
7. 上传的论文存在哪？ 是不是考虑再建一个数据表





## insert页面的json

### 基本内容

论文题目：title

发表刊物名称：conferjournalname

刊物类型：conferorjournal，c代表confer，j代表journal

发表时间：publishtime

作者们：authors，以如下形式: [{name: xxx, identity: xxx, type: xxx}, {name: xxx, identity: xxx, type: xxx}]，即列表里边套字典

论文页码起止范围：page，用列表：[开始页,结束页]

语言：language，c代表中文，e代表英文

### 额外内容，即有需要时再加入json

期刊相关：
- 卷：volume
- 期：issue
- 正刊 or 增刊：papertypeid，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人

会议相关：
- 举办国家：nation（审核页里的需求，insert页里不用）
- 举办城市：city（审核页里的需求，insert页里不用）
- 长文 or 短文 or Demo：papertypeid，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人明白即可
- Oral or Poster：papertypeid，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人明白即可


## 查询里的json

### 基本内容

最主要的那部分query：base，里面形式如下：[{title: "xxx", condition:"" },{authorname:"xxx", “condition”:"AND"}]，还有就是confername，journalname。即列表套字典。condition代表的是and或者or，如果只有一条，那么就是none

作者类型：authortype，是一个列表，就拿0，1，2来表示吧

论文类型：papertype，是一个列表，就拿0，1，2来表示吧

论文等级：paperrank，字典套列表。{ccf:['a+', 'c'], ...}

日期范围：time，用列表，[起始时间，结束时间]


