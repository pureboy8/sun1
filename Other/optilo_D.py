from sqlite3 import dbapi2
from selenium import webdriver
import time
import json
import shutil
import os,sys,re,datetime
import pdfplumber
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options # => 引入Chrome的配置
from bs4 import BeautifulSoup
from sqlalchemy import null
import win32com.client as win32
import pymssql 

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

def poname(po):    
    server="CNHSHACDC1VW023\SQLEXPRESS"
    user="sa"
    password="A8my4pai@A8my4pai@"
    database="om"
    yy='6666'
    conn=pymssql.connect(server,user,password,database)
    cursor=conn.cursor()
    #sql="select a.[Ship-To Name],b.[Name 2] from data_all_use as a inner join [kan1] as  b on a.[Ship-To ID]= b.Customer and a.po='" + po + "'"
    #cursor.execute(sql)
    cursor.execute("select a.[Ship-To Name],b.[Name 2] from data_all_use as a inner join [kan1] as  b on a.[Ship-To ID]= b.Customer and a.po=%s",(po,))
    usk=cursor.fetchall()# .fetchall()fetchone
    #print(usk.count())
    for uk in usk:
        if len(uk[1].strip())==0:
            yy=uk[0]
        else:
            yy=uk[1]

    # for uk in usk:
    #     yy=uk[1]
    cursor.close()
    conn.close()
    return yy

class DriverBuilder():

    def enable_download_in_headless_chrome(self, driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", r'C:\work\temp')#/session/$sessionId/chromium/send_command

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)
        self.logger.info("response from browser:")
        for key in command_result:
            self.logger.info("result:" + key + ":" + str(command_result[key]))
        self.options = webdriver.ChromeOptions()
        self.store_path = 'your_download_file'
        if not os.path.exists(self.store_path):
            os.makedirs(self.store_path)
        self.prefs = {'download.default_directory': self.store_path,'profile.default_content_settings.popups': 0}
        self.options.add_experimental_option('prefs', self.prefs)
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.options)
        DriverBuilder().enable_download_in_headless_chrome(self.driver, self.store_path)

def run(usr,pwd,poall,dis=0):


    global base_path
    base_path=r'C:\work\temp'
    profile = {
        'download.default_directory': base_path
        }

    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {'download.default_directory': base_path,'profile.default_content_settings.popups': 0}
    ch_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 

    #driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    driver.maximize_window() 
    url ='https://ot3.optilo.eu/opt_ext_c4rtba/p001/main.php?m=cwlib&c=login'
    driver.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver.get(url)
    time.sleep(2) 
    link=driver.find_element_by_xpath('//*[@id="inpLogin"]') 
    link.send_keys(usr)#'sylar.sun@philips.com'
    user=driver.find_element_by_xpath('//*[@id="inpPassword"]')
    user.send_keys(pwd)#'a8my4pai'

    cmd=driver.find_element_by_xpath('//*[@id="submitLogin"]')
    cmd.click()

    time.sleep(1) 
    #summary
    #driver.find_element_by_xpath('//*[@id="menu-1-163995"]/a').click()
    driver.find_element_by_link_text("Summary").click()
    WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']"))
    year=time.strftime('%Y', time.localtime(time.time()))
    yue=time.strftime('%m', time.localtime(time.time()))
    day=time.strftime('%m%d', time.localtime(time.time()))
    isExists=os.path.exists(r'Y:\IS\IDOC' + "\\" + year +"年" )
    if not isExists:
        os.makedirs(r'Y:\IS\IDOC' + "\\" + year +"年" )
    isExists=os.path.exists(r'Y:\IS\IDOC' + "\\" + year +"年" + "\\" + yue )
    if not isExists:
        os.makedirs(r'Y:\IS\IDOC' + "\\" + year +"年" + "\\" + yue )
    isExists=os.path.exists(r'Y:\IS\IDOC\2022年' + "\\" + yue + "\\" +day)
    if not isExists:
        os.makedirs(r'Y:\IS\IDOC' + "\\" + year +"年" + "\\" + yue + "\\" +day) 
    txtfile=open( r'Y:\IS\IDOC' + "\\" + year +"年" + "\\" + yue + "\\" +day + "\\" + "log.txt" , 'a')

    for  pon,values in poall:
        po=driver.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']")
        #po=driver.find_element_by_xpath('//*[@id="DF100007367_mp1_so_number"]')
        driver.execute_script("arguments[0].value = '" + pon + "';", po)
        #po.send_keys(pon)#4516773895

        driver.find_element_by_xpath('//*[@id="content_6f962c95b57247a66951fd7a883e2c27"]/div[2]/div/input[1]').click()
        time.sleep(1)
        #try:
        data1=driver.find_element_by_xpath('//*[@id="content_0a3ddf58e49fb088dc15a424277fd953"]')
        if data1.text=="No data":
            # tsheet.Range("A"+str(rowi)).Value=pon
            # tsheet.Range("B"+str(rowi)).Value="No data in optilo"
            txtfile.writelines(f"po: {pon} Can't find in Optilo,pls confirm.\n")
            print( f"po:{pon}在Optilo没有找到,请确认。")
        else:
            table1=driver.find_element_by_xpath("//*[@id='DL100007368']")

            trlist = driver.find_elements_by_xpath('//*[@id="DL100007368"]/tbody/tr') #行
            tdlist = driver.find_elements_by_xpath('//*[@id="DL100007368"]/tbody/tr/td') #列

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
            find=0
            for i in range(2,a_trn+1): #行
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[6]')
                unit=x.text[len(values):].replace("/","_")
                #print(unit)
                
                if x.text[0:len(values)]==values:
                    find=find+1
                    x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[2]')
                    driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[2]/a').click()
                    driver.switch_to.frame(0)

                    #begin files
                    #driver.find_element_by_xpath('//*[@id="mytabs0"]/ul/li[4]/a/span').click()
                    WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*[@id="mytabs0"]/ul/li[4]/a/span')).click()
                    #trlist = driver.find_elements_by_xpath('//*[@id="DP690000322"]/tbody/tr') #行
                    trlist = driver.find_elements_by_xpath('/html/body/div/div[4]/div[2]/form/div[4]/div[2]/div[2]/div/div[1]/table/tbody/tr/td[1]/div[1]/table/tbody/tr') #行
                    tdlist = driver.find_elements_by_xpath('//*[@id="DP690000322"]/tbody/tr/td') #列

                    trn = len(trlist) #总行数
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
                    tdn = sum(temlist)
                    tdn = int(tdn/trn) #总列数
                    filet=filep=filei=0
                    for i in range(2,trn+1): #行
                        #check file is pdf
                        file1=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[2]')
                        if file1.text[-3:]=='pdf':
                            m=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[2]/a')
                            n=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[5]')
                            ff=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[2]').text
                            m.click()
                            time.sleep(3)
                            while True:
                                oldname = sort_file()
                                file_type = oldname.split('.')[-1]
                                if oldname != '' and file_type != 'crdownload':
                                    #print('下载已完成')
                                    break
                                else:
                                    #print("等待下载。。。")
                                    time.sleep(2)

                            time.sleep(1)
                            if n.text.split(' ')[0]=='trace':
                                newname = "Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\T_" + poname(pon)+unit+"("+pon+")" + "." + file_type
                                filet=1
                                if find>1:
                                    newname = "Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\T_" + poname(pon)+unit+"("+pon+")" + str(find) + "." + file_type
                            else:
                                if n.text.split(' ')[0]=='pack':
                                    newname = "Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\P_" + poname(pon)+unit+"("+pon+")" + "." + file_type
                                    filep=1
                                    if find>1:
                                        newname = "Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\P_" + poname(pon)+unit+"("+pon+")"  + str(find) + "." + file_type
                                else: 
                                    if n.text.split(' ')[0]=='sales':
                                        newname ="Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\I_" + poname(pon)+unit+"("+pon+")" + "." + file_type
                                        filei=1
                                        if find>1:
                                           newname ="Y:\IS\IDOC" + "\\" + year +"年" + "\\" + yue + "\\" +day +"\\I_" + poname(pon)+unit+"("+pon+")" + str(find) + "." + file_type
                                         
                            #print('1'+ff)
                            #print('2'+oldname.split('\\')[-1])
                            if ff==oldname.split('\\')[-1]:
                                shutil.move(oldname, newname)
                                print('归档成功'+oldname+"->"+newname) 

                    #end files
                    if find ==1:
                        if filet==0:
                            print( f"po:{pon}的ITEM:{values}的trace/T文件Optilo没有找到,请确认。")
                            txtfile.writelines( f"po:{pon}->ITEM:{values}'s trace/T file Can't find.Pls Check.\n")
                        if filep==0:
                            print( f"po:{pon}的ITEM:{values}的pack/P文件Optilo没有找到,请确认。")
                            txtfile.writelines(f"po:{pon}->ITEM:{values}'s pack/P file Can't find.Pls Check.\n")
                        if filei==0:
                            print( f"po:{pon}的ITEM:{values}的sales/invoice文件Optilo没有找到,请确认。")
                            txtfile.writelines(f"po:{pon}->ITEM:{values}'s sales/invoice file Can't find.Pls Check.\n")
                        if filet==filep==filei==1:
                            print( f"po:{pon}的ITEM:{values}的PTI下载完了。")
                            txtfile.writelines(f"po:{pon}->ITEM:{values}'s PTI Download Complete.\n")
                    
                    try:
                        driver.switch_to.default_content()
                    except:
                        pass
                    driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()
                    driver.switch_to.default_content()
            if find ==0:
                print( f"po:{pon}的ITEM:{values}在Optilo没有找到,请确认。")
                txtfile.writelines( f"po:{pon}'s:{values}can't find in Optilo,pls comfirm。")
        # except:
        #     rowi=rowi+1
        # finally:
        #     pass
    txtfile.close()
    driver.quit()

if __name__=='__main__':
    #print(poname('4517481334'))
    filepath=r"C:\Users\320144297\Philips\RPA for Daily IDOC(JP OM) - PDF"
    a={}
    os.system('net use y: \\CNHSZHPHC1MS002\Order Management')
    b=[]
    tt2=time.strftime('%Y-%m-%d', time.localtime(time.time()))
    c=input('You can Input the date you want to download PTI.The format is(yyyy-mm-dd) defalt:Today?')
    if c=="":
        c=tt2    
    #print(c)
    f = open('1.txt','r')
    z = list(f)
    f.close()
    filelist = os.listdir(filepath)
    for  f in filelist:
        t=os.path.getmtime(filepath + "\\"+ f)
        #t = os.path.getmtime('b.json')
        timeStruce = time.localtime(t)
        times = time.strftime('%Y-%m-%d', timeStruce)
        
        if f[-3:]=="pdf" and times==c:
            with pdfplumber.open(filepath + "\\"+ f) as pdf:
                txt=pdf.pages[0].extract_text()
                #print(txt)
                checkIM = r"(45\d*) (.*)PCE"
                id1=re.findall(checkIM, txt)
                b.append([id1[0][0],id1[0][1].split(' ')[-2]])
                #print(b)
    # b=[['4517283258','782107']]
    # run(z[0],z[1],b)
    if b !=[]:
        run(z[0],z[1],b)
