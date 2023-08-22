import pymssql
server="CNHSHACDC1VW023\SQLEXPRESS"
user="sa"
password="A8my4pai@A8my4pai@"
database="om"
conn=pymssql.connect(server,user,password,database)
cursor=conn.cursor()
sql="select  * from so_ship "
cursor.execute(sql)
usk=cursor.fetchall()
for uk in usk:
    print(uk[0],uk[1])
# sql="update "
# conn.commit()
conn.close()