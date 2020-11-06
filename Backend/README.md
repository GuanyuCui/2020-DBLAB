## 安装django
```shell
python -m pip install Django
```
## mysql操作
###  读取现有数据表
1. 在```/Backend/Backend/settings.py```中修改**数据库名称、用户、密码**
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
5. 访问`http://127.0.0.1:8000/demo`
  