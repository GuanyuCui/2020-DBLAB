## Instruction
1. 安装django, pymysql, mysqlclient...
   ```shell
    pip3 install Django pymysql mysqlclient
   ```
2. 在mysql数据库中创建一个database，名为`BBS`
   ```sql
   CREATE DATABASE BBS;
   ```
3. 将root用户密码改为空
   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED WITH MYSQL_NATIVE_PASSWORD BY '';
   ```
4. ```shell
    cd (GitHub repo 地址)/2020-DBLAB/Research_Management
   ```
5. ```shell
    python3 manage.py makemigrations
   ```
6. ```shell
    python3 manage.py migrate
   ```
7. ```shell
    python3 manage.py runserver
   ```
8. 浏览器访问`http://127.0.0.1:8000/home`

### 如果报错`require mysqlclient >= 1.4.0`
- 查看自己django的安装目录，我的是`'D:\\apps\\Anaconda\\envs\\web\\lib\\site-packages\\django`，记得去掉最后的`__init__.py`
  ```shell
  python3
  >> import django
  >> print(django.__file__)
  ```
- 文件资源管理器中找到相应目录并打开
- 打开`django/db/backends/mysql/base.py`
- 注释掉下面两行
  ```python
    if version < (1, 4, 0):
        raise ImproperlyConfigured('mysqlclient 1.4.0 or newer is required; you have %s.' % Database.__version__)
  ```