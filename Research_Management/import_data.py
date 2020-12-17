import pymysql
import pandas
def import_confer(file_path):
    """
        导入会议
    """
    # 打开数据库连接
    db = pymysql.connect("localhost","root","","Research_Management")
    data = pandas.read_csv(file_path)
    data = data.drop_duplicates(subset=['学校全称'])
    data = data.dropna(subset=['学校全称'],how='any')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for i,v in data.iterrows():
        try:
            cursor.execute("insert into conferjournal values(\"%s\",\"c\",\"%s\",\"%s\",\"%s\",\"%s\",'');" % (v['学校全称'].strip(), v['学校简称'], v['学校等级'], v['CCF等级'], v['CCF等级']))
            db.commit()
        except:
            print("Error in : insert into conferjournal values('%s','c','%s','%s','%s','%s','');" % (v['学校全称'].strip(), v['学校简称'], v['学校等级'], v['CCF等级'], v['CCF等级']))
    
def import_author(file_path):
    """
        导入教师
    """
    db = pymysql.connect("localhost","root","","Research_Management" )
    data = pandas.read_csv(file_path)
    data = data.drop_duplicates(subset=['职工号'])
    data = data.dropna(subset=['职工号'],how='any')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    for i,v in data.iterrows():
        try:
            cursor.execute("insert into author values(\"%s\",\"%s\");" % (v['职工号'],v['姓名']))
            db.commit()
        except:
            print("Error in : insert into author values(\"%s\",\"%s\");" % (v['职工号'],v['姓名']))

if __name__ == "__main__":
    import_author('static/basic-data/authors.csv')
    import_confer('static/basic-data/conferences.csv')
