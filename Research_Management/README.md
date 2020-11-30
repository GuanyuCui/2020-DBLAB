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


**返回数据的例子:**
```python
data_post = {
    "title":"Personalized News Recommendation with Context Trees",
    "papertypeid":"1",
     ...
}
```

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
- 正刊 or 增刊：cjtype，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人

会议相关：
- 举办国家：nation（审核页里的需求，insert页里不用）
- 举办城市：city（审核页里的需求，insert页里不用）
- 长文 or 短文 or Demo：cjtype，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人明白即可
- Oral or Poster：cjtype，这里前端人员自己内部定一下，然后在这里写一下，让做后端的人明白即可


## 查询里的json

### 基本内容

最主要的那部分query，里面形式如下：[{key: "xxx", value:"xxx",condition:"" }...]，还有就是confername，journalname。即列表套字典。condition代表的是and或者or，如果只有一条，那么就是空字符串

作者类型：authortype，是一个列表，就拿0，1，2来表示吧
`
论文类型：papertype，是一个列表，就拿0，1，2来表示吧

论文等级：paperrank，字典套列表。{ccf:['a+', 'c'], ...}

日期范围：time，用列表，[起始时间，结束时间]


## Bugs

### 用户 
1. 登录页
   - [ ] index点完登录后不要一直登陆中 **done**
2. createuser
   - [ ] createuser页不能输入超过8个字符
   - [ ] admin页创建的用户无法在index页登录
   - [ ] index页刷新会自动登录管理员账号

### 前后端
1. insert页
   - [ ] （最后再做）确认信息
   - [x] （AUTO field解决？）用全局变量维护paperid有问题, 要不然新插入的会覆盖原来插入的
   - [x] 提交论文的前端按钮偏移
   - [x] keywords (不管)
   - [x] 期刊没有插入卷期
   - [x] 作者按顺序排(第一、第二):insert页的独立作者改为普通作者, 如果只有一个普通作者, 则默认是独立作者
   - [ ] （请后端做一下，谢谢）插入成功后页面的跳转

2. query页
   - [x] 不选也可以提交
   - [x] and or顺序逻辑
   - [x] 用户只能查自己参与的论文, 那就不需要作者姓名的选项
   - [x] 管理员可以查所有论文才需要作者姓名的选项
   - [ ] 各种页面头顶的scripts啥的一堆链接那都是啥？
   - [ ] query页无法点击**更多操作**按钮
   - [ ] 管理员登录的时候默认显示的query条件全都是作者姓名

## TODO
### 数据库
1. 临时表
   - [x] paper临时表不要有外码
   - [x] 临时pa表加author type
   - [ ] 增加check, 保证pa表的作者名一定在author表中有对应

2. 基本表
   - [x] conferorjournal需要存么？

### 前后端
1. 主页
   - [x] 删除功能

2. 查询页
   - [ ] 查询成功后返回的结果要啥样, 添加点击按钮, 链接详情页
   - [ ] 顶部的查询栏, 第一栏为空则不能添加别的栏
   - [ ] 查询页是否有必要添加authorrank的查询？ 针对管理员
     - 只能处理查询A和B都是第一作者(如果在顶部的query中指明作者姓名为A or B)的论文
     - 无法处理 管理员 查询 A 是第一作者, B 是通讯作者的论文

3. 审核页 修改页
   - [ ] 不要让用户重复上传, 应该自动加载用户上传的文件, 增加下载按钮

3. 插入页 
   - [ ] 后端 ID 部分可以去掉了

### 用户
1. 登录页
   - [ ] 验证码改4位
2. 用户相关
   - [ ] 给张老师一个id, createsuperuser给他自己一个账号
   - [ ] 主页上显示用户的名字？

### 代码结构
- [ ] 在view中区分整理api和页面的位置

## 问题
- 处理query的时候如果查到一半发现是空集就直接返回？