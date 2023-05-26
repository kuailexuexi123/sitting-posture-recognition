import pymysql
with open('D:\pythonProject5\PyQt5_yemian\结果存放', "r", encoding='utf-8') as file_obj:
    contents = file_obj.read()
    x = contents.split("-")
    yonghu_name = x[0]
    yonghu_password = x[1]  # 未完善
    print(yonghu_name)
conn = pymysql.connect(host='localhost', port=3306, user='root', password='nuliba520.', db='test')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users WHERE username=%s ', yonghu_name)
result = cursor.fetchall()
for row in result:
    yonghu_name = row[0]
    yonghu_password=row[1]
    yonghu_number=row[2]
    yonghu_email=row[3]
print(yonghu_name,yonghu_password,yonghu_number,yonghu_email)