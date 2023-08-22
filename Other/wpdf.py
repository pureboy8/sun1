from PyPDF2 import PdfFileReader,PdfFileWriter 
import pdfplumber
import re,os
import pymssql
def soname(so):    
    server="CNHSHACDC1VW023\SQLEXPRESS"
    user="sa"
    password="A8my4pai@A8my4pai@"
    database="om"
    yy='6666'
    conn=pymssql.connect(server,user,password,database)
    cursor=conn.cursor()
    sql="select  * from so_ship where so='" + so + "'"
    cursor.execute(sql)
    usk=cursor.fetchall()
    for uk in usk:
        yy=uk[1]
    
    conn.close()
    return yy

list1=os.listdir(r'C:/Users/320144297/OneDrive - Philips/Email attachments from Power Automate/Billing/')
for file in list1:
    #print(file[-3:])
    if file[-3:] == "pdf":
        openfile=r'C:/Users/320144297/OneDrive - Philips/Email attachments from Power Automate/Billing/'+file
        with pdfplumber.open(openfile) as pdf:
            data= pdf.pages[0].extract_text()
            #print(data)
            checkIM = r"参照番号：.(\d+)"
            id1=re.search(checkIM, data).group(1) 
            r=soname(id1)
            #print(type(id1))   
            # checkIM = r"(.*(病院|医療)).*"
            # r = re.findall(checkIM,data,re.M)[-1]
            # print(type(r[0]))
            # print(type(r[0])=="<class 'str'>")
            # if type(r) !="str":
            #     r=r[0]
            checkIM = r"検収書"
            id2=re.findall(checkIM, data)
            #print(id2[0])
        isExists=os.path.exists(r'C:/work/Billing/ZPO/2022/6/'+ id1  )
        if not isExists:
            os.makedirs(r'C:/work/Billing/ZPO/2022/6/'+ id1  )    
        pdfreader = PdfFileReader(openfile)
        if pdfreader.getNumPages()==1 or id2=='':
            #os.remove('C:/work/Billing/ZPO/2022/6/' + id1 + '/' + id1 + ' ' + r + ' 検収書.pdf')
            os.rename( openfile, 'C:/work/Billing/ZPO/2022/6/' + id1 + '/' + id1 + ' ' + r + ' 検収書.pdf')
            
        else:
            for page in range(pdfreader.getNumPages()): # getNumPages()获取总页数
                wpdf = PdfFileWriter()  # 实例化对象
                wpdf.addPage(pdfreader.getPage(page)) # 将遍历出的每一页添加到实例化对象中
                wpdf.addMetadata()
                if page == 0 :
                    filename = id1 + ' ' + r + ' 請求書.pdf'
                else:
                    filename = id1 + ' ' + r + ' 納品書.pdf'
                with open(f'C:/work/Billing/ZPO/2022/6/' + id1 + '/' + filename  , "wb") as f:
                    wpdf.write(f)

