*last update：2020.12.5*

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
1. createuser
   - [ ] admin页创建的用户无法在index页登录 -> snl
   - [ ] 创建用户后，若author表没有，应当插入 -> zpt

### 前后端
1. insert页
   - [x] autoincrease无法回退就会一直加
      - 检查当表为空，重新设置起点为1
      - SQL 语句该字段改成 bigint -> zcy
   - [ ] BibTeX 框大一点
   - [ ] CCF 等级只有 ABC
   - [ ] 默认选中长文

2. query页
   - [ ] CCF 等级只有 ABC

3. detail页
   - [ ] 缺少部分信息的显示 -> 应该按 excel 格式做
   - [ ] 会议前端仍有卷期问题 -> wsx

## TODO
### 数据库
1. 临时表
   - [x] title 字段太短，需要增长 -> zcy

2. 基本表

### 前后端
1. 主页
   - [ ] tmp表是否应当增加提交时间，方便显示？
      - 还是说已经根据ID排了？
2. 查询页

3. 审核页 修改页
   - [ ] 不要让用户重复上传, 应该自动加载用户上传的文件, 增加下载按钮 -> zpt
   - [ ] 审核页应当删除tmp表的项目 -> wsx

4. 插入页 
   - [ ] 输入期刊、会议名称，跳出提示 -> cgy
   - [ ] 输入教师姓名，跳出提示 -> cgy
   - [ ] 插入失败的提示？比如不在作者表里？-> ?

### 代码结构
- [ ] 在view中区分整理api和页面的位置

### 实验报告
- [ ] ER 图/数据字典的问题 -> zcy
- [ ] 系统测试部分 
   - 登录页 -> cgy
   - 主页 -> cgy
   - 插入页 -> wsx
   - 修改页 -> zcy
   - 审核页 -> zpt
   - 查询页/详情页 -> snl
   - 创建新用户 -> cgy

### PPT展示
- [ ] 几个部分？