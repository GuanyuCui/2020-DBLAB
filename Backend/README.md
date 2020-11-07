## 安装django
```shell
python -m pip install Django
```
**短篇幅很难说清哪个文件是干嘛的，建议访问[官网](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)看教程**
## Set up
1. 在```/Backend/Backend/settings.py```中修改**数据库名称、用户、密码**
   - 我是新建了一个库叫**db**，里面只有一张表**Demo**
     - `CREATE TABLE DEMO(paperID INT PRIMARIKY KEY, content CHAR(50))`，然后随便插入了几条数据
   - 最好咱们五个同一，每个人都用root，密码123456，同样的数据库
2. ```shell
   cd /Backend
   ```

3. ```shell
   # 将数据表的更改作为migration存储
   python manage.py makemigrations 
   ```
4. ```shell
   # 应用更改到django中
   python manage.py migrate demo
   ```
5. ```shell
   python manage.py runserver
   ```
6. 访问`http://127.0.0.1:8000/demo/`、`http://127.0.0.1:8000/demo/1`，`http://127.0.0.1:8000/demo/2`
   - 这个`demo/x`的x取决于数据库里有多少条数据
   - 可以在输入框输入内容后提交
  