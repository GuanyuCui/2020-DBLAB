## 后端

*last update：2020.11.13*

### 已实现

**页面部分**

home

register（但没有作为页面加入路由，原因是因为以后将作为单页面应用嵌入主页）

login

*默认管理员为admin，密码也是admin*

**API部分**

获取验证码

**TODO**

1.  查询、注册、添加论文页面的嵌入及过程中API的编写

2.  总体完成后开始区分管理员与普通用户的功能区别

## 前端

**TODO**

1.  将templates/home.html抽象成一个base.html，base.html中要留出content的接口，并且修改成适合我们的样式，如只保留左侧列，目前是只保留顶栏，而且格式有问题
2.  最好能做一个index页面，然后把login.html和其整合在一起，就像obe一样，现在的login有点丑，以后的逻辑我设想的是一进来就是一个index页，然后登入进入home