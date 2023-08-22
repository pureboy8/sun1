from selenium import webdriver
import time
import json
import shutil,os,re
import pdfplumber
import requests
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from sqlalchemy import null
import win32com.client as win32
def sort_file():
    # 排序文件
    dir_link = base_path
    dir_lists = list(filter(check_file, os.listdir(dir_link)))
    if len(dir_lists) == 0:
        return ''
    else:
        dir_lists.sort(key=lambda fn: os.path.getmtime(dir_link + os.sep + fn))
        return os.path.join(base_path, dir_lists[-1])

def check_file(filename):
    # 忽略系统文件
    if filename == '.DS_Store' or filename == 'thumbs.db':
        return False
    global base_path
    # 排除文件夹
    return os.path.isfile(os.path.join(base_path, filename))

def dowload(so):
    global base_path
    base_path=r'C:\work\temp'
    ch_options = Options()
    #ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.minimize_window() 
    url2 ='https://pww.comopsdms.healthcare.philips.com/livelink/llisapi.dll?func=ll&objtype=258&objAction=GetAdminTemplate&adminUserTemplateSelected=Order%20Package%20Japan'
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }
              
    driver2.get(url2)
    input=WebDriverWait(driver2,30).until(lambda x: x.find_element_by_xpath('//*[@id="fieldquery"]/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[5]/td[3]/input'))
    input.send_keys(so)
    submit=WebDriverWait(driver2,30).until(lambda x: x.find_element_by_xpath('//*[@id="searchBtnMiddle"]/a'))
    submit.click()
    result1=WebDriverWait(driver2,30).until(lambda x: x.find_element_by_xpath('//*[@id="resultlist2"]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/span/a'))
    result1.click()
    driver2.find_element_by_xpath('//a[text()="01. 必須書類"]').click()
    # 网址 = driver2.current_url
    # UA伪装="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    # cookies = driver2.get_cookies()
    # cookie_dict = {}
    # for i in cookies:
    #     cookie_dict[i["name"]] = i["value"]
    # 响应数据 = requests.get(url=网址,headers=UA伪装,cookies=cookie_dict).text
    # 解析 = etree.HTML(响应数据)
    # print(解析)

    trlist = driver2.find_elements_by_xpath('//*[@id="browseViewCoreTable"]/tbody/tr') #行
    tdlist = driver2.find_elements_by_xpath('//*[@id="browseViewCoreTable"]/tbody/tr/td') #列
    a_trn = len(trlist) #总行数
    #print(a_trn)
    temlist = []
    for td in tdlist:
        try:
            temlist.append(int(td.get_attribute('colspan')))
        except:
            temlist.append(1)
        try:
            temlist.append(int(td.get_attribute('rowspan'))-1)
        except:
            pass
    a_tdn = sum(temlist)
    a_tdn = int(a_tdn/a_trn) #总列数
    for i in range(2,a_trn+1): #行
        x= driver2.find_element_by_xpath('//*[@id="browseViewCoreTable"]/tbody/tr[' + str(i) + ']/td[3]/a')
        if x.text[0:2]=="受注":
            x.click()
            # print(x.get_attribute('href'))
            # lk=x.get_attribute('href')
            # headerss= {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
            # data = requests.get(url=lk, headers=headerss).content
            # with open(r'C:\work\Billing\ZPO\2022\4' + '\\'+ so+'\\a.pdf', 'wb') as f:
            #         f.write(data)
            #         print('a', '下载成功！！！')

            oldname='C:/Users/320144297/Downloads/' + x.text.strip()
            y=0
            while not os.path.isfile(oldname) or y>40:
                time.sleep(2)
                y+=1
            #time.sleep(40)
            # while True:
            #     f= list(filter(x.text.strip(), os.listdir('C:/Users/320144297/Downloads/')))
            #     if f[-1]=='pdf':
            #         print(f)
            #         break
            #     else:
            #         print(f)
            #         time.sleep(2)
            # oldname = sort_file()
            #     file_type = oldname.split('.')[-1]
            #     if oldname != '' and file_type != 'crdownload':
            #         #print('下载已完成')
            #         nn=oldname
            #         break
            #     else:
            #         #print("等待下载。。。")
            #         time.sleep(2)
            pp=r'C:\work\Billing\ZPO\2022\5' + '\\'+ so 
            isExists=os.path.exists(pp )
            
            if not isExists:
                os.makedirs(pp)         
            newname = pp + '\\' + x.text.strip()
            # #os.rename(oldname, newname)
            shutil.move(oldname, newname)
            #print(oldname)
            #print(newname)
            #os.rename(oldname, newname)
            filelist=os.listdir( pp + '\\' )
            pdfname=1
            # for f in filelist:
            #     a=f.replace("　","")
            #     os.rename(f,a)
            for f in filelist:
                if f[-3:]=="pdf" : #and f[0:5] != '受注後変更'
                    #print(pp + '\\' + f)
                    with pdfplumber.open( pp + '\\' + f) as pdf:
                        txt=pdf.pages[0].extract_text()
                        # print(txt)
                        checkIM = r"先） (.*) 顧"
                        id1=re.search(checkIM, txt)
                        a= id1.group(1) 
                        checkIM = r"メールアドレス (.*)\n"
                        id1=re.search(checkIM, txt)
                        if id1 == None:
                            b= ''
                        else:
                            b=id1.group(1) 
                        checkIM = r"契約先名 (.*) 顧客"
                        id1=re.search(checkIM, txt)
                        
                        checkIM = r"契約先担当者名(.*)"
                        id2=re.search(checkIM, txt)
                        c= id1.group(1)+" " +id2.group(1) 
                        checkIM = 'その他(.*)'
                        id1=re.findall(checkIM, txt)
                        d= id1[-1].strip()
                        
                        checkIM = r"担当営業名 (.*) "
                        id1=re.search(checkIM, txt)
                        e= id1.group(1) 
                        with open(pp + '\\' + str(pdfname) + '.txt', 'w') as f:
                            f.write(a + "\n")
                            f.write(b + "\n")
                            f.write(c + "\n")
                            f.write(d + "\n")
                            f.write(e + "\n")
                        pdfname +=1


    driver2.quit()



if __name__=='__main__':    
    # global base_path
    # base_path=r'C:\work\temp'
    #a=dowload('6600547235')
    f = open('so.txt','r')
    b=[i.replace("\n", "") for i in f]
    f.close()
    for x in b:
        dowload(x)
