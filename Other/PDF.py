import pdfplumber
import pandas as pd
import re,os,time
from PyPDF2 import PdfFileReader,PdfFileWriter 
filepath=r"C:\Users\320144297\Philips\RPA for Daily IDOC(JP OM) - PDF"
a={}
filelist = os.listdir(filepath)
for  f in filelist:
    t=os.path.getmtime(filepath + "\\"+ f)
    #t = os.path.getmtime('b.json')
    timeStruce = time.localtime(t)
    times = time.strftime('%Y-%m-%d', timeStruce)
    #print(times)
    if f[-3:]=="pdf" and times=='2022-05-13':
        with pdfplumber.open(filepath + "\\"+ f) as pdf:
            txt=pdf.pages[0].extract_text()
            #print(txt)
            checkIM = r"(45\d*) (.*)PCE"
            id1=re.findall(checkIM, txt)
            #print(id1[0][0])
            #print(id1[0][1].split(' ')[-2])
            a.update({id1[0][0]:id1[0][1].split(' ')[-2]})
for key,value in a.items():
    print(f"key{key},value{value}")
    # for tb in pdf.pages[0].extract_tables():
    #      data=pd.DataFrame(tb[1:],columns=tb[1])
    #      print(data)
         #data.to_excel(f'c:/work/{0+1}.xlsx' ,encoding="shift-jis")
# Contents.DrawText(Comic, 40.0, 4.25, 9.25, TextJustify.Center, 0.02, Color.FromArgb(128, 0, 255), Color.FromArgb(255, 0, 128), "PDF FILE WRITER");
# Contents.SaveGraphicsState();
# Contents.SetColorNonStroking(Color.Purple);
# Contents.DrawText(Comic, 30.0, 4.25, 8.75, TextJustify.Center, "Example");
# Contents.RestoreGraphicsState();
 
 
# Contents = new PdfContents(Page);


# path=r'C:\work\Billing\ZPO\2022\5\6600549767'

# filepath=path + "\\" +"受注伝票-広島市立安佐市民病院_救命センターモニタリングシステム　19式.pdf"
# filelist=os.listdir( path + '\\' )

# # for f in filelist:
# #     print(f)

# with pdfplumber.open(filepath) as pdf:
#     txt=pdf.pages[0].extract_text()
#     #print(txt)
#     checkIM = r"先） (.*) 顧"
#     id1=re.search(checkIM, txt)
#     a= id1.group(1).strip()
#     checkIM = r"メールアドレス (.*)\n"
#     id1=re.search(checkIM, txt)
#     if id1 == None:
#         b=''
#     else:
#         b= id1.group(1) 
    
#     checkIM = r"契約先名(.*)顧客"
#     id1=re.search(checkIM, txt)
    
#     checkIM = r"契約先担当者名(.*)"
#     id2=re.search(checkIM, txt)
#     c= id1.group(1).strip()+" " +id2.group(1).strip() 
#     checkIM = 'その他(.*)'
#     id1=re.findall(checkIM, txt)
#     d= id1[-1].strip()
#     checkIM = r"担当営業名 (.*) "
#     id1=re.search(checkIM, txt)
    
#     e= id1.group(1) 
#     #print(e)
#     with open(path +'\\' + '1.txt', 'w') as f:
#         f.write(a+"\n")
#         f.write(b+"\n")
#         f.write(c+"\n")
#         f.write(d+"\n")
#         f.write(e+"\n")

   # for tb in pdf.pages[0].extract_tables():
   #       data=pd.DataFrame(tb[1:],columns=tb[1])
   #       #print(data)
   #       data.to_excel(f'c:/work/{0+1}.xlsx' ,encoding="shift-jis")

   # print(pdf.pages[0].extract_tables()[0][1][2])
   # print(pdf.pages[0].extract_tables()[0][2][2])
   # print(pdf.pages[0].extract_tables()[2][0][1])
   # print(pdf.pages[0].extract_tables()[2][0][3])
   # for page in pdf.pages:
   #    txt = page.extract_text()
   #    print(txt)