from selenium import webdriver
import time
import json
import shutil
import os,sys
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options # => 引入Chrome的配置
from bs4 import BeautifulSoup
import win32com.client as win32
a = '' 
b = ''
choice = ''

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

def findritong(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 在启动浏览器时加入配置
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.maximize_window() 
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver2.get(url2)
    no_ship=url2[-12:]
    #time.sleep(3) 
    WebDriverWait(driver2,10).until(lambda x: x.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/span'))

    ac=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/span')
    #tsheet.cells(rowi,3).Value=ac.text
    ad=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div[2]/span')
    #tsheet.cells(rowi,4).Value=ad.text
    nc=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[2]/span')
    #tsheet.cells(rowi,5).Value=nc.text
    nd=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div[2]/span')
    #tsheet.cells(rowi,6).Value=nd.text
    #twb.SaveAs(targetfile)
    driver2.quit()

def findfrex(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 在启动浏览器时加入配置
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.maximize_window() 
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver2.get(url2)
    #time.sleep(4)
    WebDriverWait(driver2,10).until(lambda x: x.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]'))
    
    ac=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]')
    
    ad=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[2]')
    
    aa=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[1]')
    
    ab=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[2]/span')
    
    #tsheet.cells(rowi,3).Value=ac.text
    
    #tsheet.cells(rowi,4).Value=ad.text
    
    #tsheet.cells(rowi,5).Value=aa.text
    
    #tsheet.cells(rowi,6).Value=ab.text
    #twb.SaveAs(targetfile)
    driver2.quit()

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

def ask():
    msg='''
        1 High Speed With Excel Not Show realtime
            System will get the ETD/ETA data from optilo
        2 High Speed With  Show Excel  realtime
            System will get the ETD/ETA data from optilo
        3 Low Speed With Excel Not Show realtime
            System will get the ETD/ETA data from Internet
        4 Low Speed With Show Excel  realtime
            System will get the ETD/ETA data from Internet
        
        You can select within 10's ,Default is 1
        
        0 exit
        '''
    print(msg)
    choice = input("Tell your select, you have 5 seconds:  ")
    #print("ok1")
    if choice =="0":
        os._exit(1)
    run(a[0],a[1],b,choice)
    #exit(exit_message)
    os._exit(1)

def exit(msg):
    """
    Exit function, prints something and then exits using OS
    Please note you cannot use sys.exit when threading..
    You need to use os._exit instead
    """
    #print(msg)
    #print("ok2")
    
    os._exit(1)

def close_if_time_pass(seconds):
    time.sleep(seconds)
    #exit("Time passed, I still don't know your name..")
    #run(a[0],a[1],b,1)
    if choice == '':
        run(a[0],a[1],b,1)
    os._exit(1)


def maersk(ur):
    ch_options = Options()
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.minimize_window() 
    url2 ='https://www.maersk.com.cn/tracking/' + ur
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver2.get(url2)
    time.sleep(1)
    try:
        #WebDriverWait(driver2,3).until(lambda x: x.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/dl/dd[1]'))
        #driver2.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/dl/dd[1]')
        ac=driver2.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/dl/dd[1]').text
        ad=driver2.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/dl/dd[2]').text
    except:
        ac=''
        ad=''
    return(ac,ad)

    driver2.quit()

def dsv(ur):
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 在启动浏览器时加入配置
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.maximize_window() 

    url2 ='https://mydsv.com/track-shipment'

    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  

    cookie_path = 'cookie.txt'

    with open(cookie_path, 'r', encoding='utf-8') as f:
        cookies = f.readlines()
    driver2.get(url2)
    
    for cookie in cookies:
        cookie=cookie.replace(r'\n', '')
        cookie_li = json.loads(cookie)
        for cookie in cookie_li:
            driver2.add_cookie(cookie)
        driver2.refresh()	

    x=WebDriverWait(driver2,3).until(lambda x: x.find_element_by_xpath('//*[@id="shipments"]'))
    x.send_keys( ur + Keys.ENTER)
    ac=WebDriverWait(driver2,10).until(lambda x: x.find_element_by_xpath('//*[@id="fullpage"]/div/div[1]/div[3]/div/div/milestone-box[1]/div/div/div/div[2]/div[2]/shipment-date/div'))
    ad=driver2.find_element_by_xpath('//*[@id="fullpage"]/div/div[1]/div[3]/div/div/milestone-box[2]/div/div/div/div[2]/div[2]/shipment-date/div')
    return(ac.text,ad.text)
    driver2.quit()

def run(usr,pwd,poall,dis=0):
    excel=win32.DispatchEx('Excel.Application')
    if  dis=="1" or dis=="3":
        excel.Visible = 0
    else:
        excel.Visible = 1
    #twb=excel.Workbooks.Open(rfile)
    twb=excel.Workbooks.Add()
    tsheet=twb.Worksheets(1)
    if dis=="3" or dis=="4":
        head=[["SO"],["B/L no"],["Vessel no"],["HAWB no"],["bak"],["ETD"],["ETA"],["Meatil"],["QTY"],["Desc"]]
        for i in range(1,11):
            tsheet.cells(1,i).Value=head[i-1]
    else:
        head=[["SO"],["B/L no"],["Vessel no"],["HAWB no"],["bak"],["Departure Plan"],["Departure Actual"],["Meatil"],["QTY"],["Desc"],["Arrival Plan"],["Arrival Actual"],["Delivered Plan"],["Delivered Actual"]]
        for i in range(1,15):
            tsheet.cells(1,i).Value=head[i-1]


    rowi=2
    rowj=1
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
    driver.maximize_window() 
    url ='https://ot3.optilo.eu/opt_ext_c4rtba/p001/main.php?m=cwlib&c=login'
    driver.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver.get(url)
    time.sleep(1) 
    link=driver.find_element_by_xpath('//*[@id="inpLogin"]') 
    link.send_keys(usr)#'sylar.sun@philips.com'
    user=driver.find_element_by_xpath('//*[@id="inpPassword"]')
    user.send_keys(pwd)

    cmd=driver.find_element_by_xpath('//*[@id="submitLogin"]')
    cmd.click()

    time.sleep(1) 
    #summary
    driver.find_element_by_xpath('//*[@id="menu-1-163995"]/a').click()

    WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*[@id="DF100007367_mp1_so_number"]'))

    for  son in poall:
        so=driver.find_element_by_xpath('//*[@id="DF100007367_mp1_so_number"]')
        driver.execute_script("arguments[0].value = '" + son + "';", so)
        #po.send_keys(pon)#4516773895

        driver.find_element_by_xpath('//*[@id="content_6f962c95b57247a66951fd7a883e2c27"]/div[2]/div/input[1]').click()

        time.sleep(1) 

        #try:
        data1=driver.find_element_by_xpath('//*[@id="content_0a3ddf58e49fb088dc15a424277fd953"]')
        if data1.text=="No data":
            tsheet.cells(rowi,1).Value=son
            tsheet.cells(rowi,2).Value="No data in optilo"
            rowi=rowi+1
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
            tsheet.cells(rowi,1).Value=son

            for i in range(2,a_trn+1): #行
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[6]')
                tsheet.cells(rowi,10).Value=x.text
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]')
                
                if x.text[0:3]=='MJB':
                    #print(x.text)
                    y =driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[1]/a')
                    #time.sleep(1)
                    y.click()
                    #WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*[@id="TB_iframeContent"]'))
                    try:
                        driver.switch_to.frame(0)
                    except:
                        pass 
                    l1=WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*[@id="DF100007361_mbl_leg_1"]'))#B/L no
                    tsheet.cells(rowi,2).Value=l1.get_attribute("value")
                    l2=driver.find_element_by_xpath('//*[@id="DF100007361_hawb_leg_1"]')#Vessel no
                    tsheet.cells(rowi,3).Value=l2.get_attribute("value")
                    l3=driver.find_element_by_xpath('//*[@id="DF100007361_vessel_no_Leg1"]')#HAWB no
                    tsheet.cells(rowi,4).Value=l3.get_attribute("value")
                    if dis=="3" or dis=="4":
                        if l3.get_attribute("value")[-6:]=='MAERSK':
                            wuliu=maersk(l1.get_attribute("value"))
                            tsheet.cells(rowi,6).Value=wuliu[0]
                            tsheet.cells(rowi,7).Value=wuliu[1]
                        if l2.get_attribute("value")[:3]=="UDF":
                            wuliu=dsv(l2.get_attribute("value"))
                            tsheet.cells(rowi,6).Value=wuliu[0]
                            tsheet.cells(rowi,7).Value=wuliu[1]
                    else:
                        trlist = driver.find_elements_by_xpath('//*[@id="DL100007364"]/tbody/tr') #行
                        tdlist = driver.find_elements_by_xpath('//*[@id="DL100007364"]/tbody/tr/td') #列

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
                        for q in range(2,trn+1): #行
                            m=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[1]')
                            if m.text=="MLG500":
                                s1=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[4]').text
                                if tsheet.cells(rowi,6).Value is None:
                                    tsheet.cells(rowi,6).Value = s1
                                else:
                                    tsheet.cells(rowi,6).Value = str(tsheet.cells(rowi,6).Value) + s1
                                s2=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[5]').text
                                if tsheet.cells(rowi,7).Value is None:
                                    tsheet.cells(rowi,7).Value = s2
                                else:
                                    tsheet.cells(rowi,7).Value = str(tsheet.cells(rowi,7).Value) + s2

                            if m.text=="MLG550":
                                s1=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[4]').text
                                if tsheet.cells(rowi,10).Value is None:
                                    tsheet.cells(rowi,10).Value = s1
                                else:
                                    tsheet.cells(rowi,10).Value = str(tsheet.cells(rowi,10).Value) + s1
                                s2=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[5]').text
                                if tsheet.cells(rowi,11).Value is None:
                                    tsheet.cells(rowi,11).Value = s2
                                else:
                                    tsheet.cells(rowi,11).Value = str(tsheet.cells(rowi,11).Value) + s2
                            if m.text=="MLT600":
                                s1=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[4]').text
                                if tsheet.cells(rowi,12).Value is None:
                                    tsheet.cells(rowi,12).Value = s1
                                else:
                                    tsheet.cells(rowi,12).Value = str(tsheet.cells(rowi,12).Value) + s1
                                s2=driver.find_element_by_xpath('//*[@id="DL100007364"]/tbody/tr[' + str(q) + ']/td[5]').text
                                if tsheet.cells(rowi,13).Value is None:
                                    tsheet.cells(rowi,13).Value = s2
                                else:
                                    tsheet.cells(rowi,13).Value = str(tsheet.cells(rowi,12).Value) + s2

                    trlist = driver.find_elements_by_xpath('//*[@id="DL100007365"]/tbody/tr') #行
                    tdlist = driver.find_elements_by_xpath('//*[@id="DL100007365"]/tbody/tr/td') #列

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
                    for q in range(2,trn+1): #行
                        m=driver.find_element_by_xpath('//*[@id="DL100007365"]/tbody/tr[' + str(q) + ']/td[4]')
                        n=driver.find_element_by_xpath('//*[@id="DL100007365"]/tbody/tr[' + str(q) + ']/td[6]')
                        if len(str(m.text))>0:
                            tsheet.cells(rowi,8).Value="'" + str(m.text)
                            tsheet.cells(rowi,9).Value=n.text[0:len(n.text)-5]
                            rowi=rowi+1
                    rowi=rowi-1 #数据会多一行空的，奇怪
                                    
                    try:
                        driver.switch_to.default_content()
                    except:
                        pass
                    driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()
                    driver.switch_to.default_content()

                    
                    

    driver.quit()
    excel.Visible = 1

if __name__=='__main__':    
    f = open('1.txt','r')
    a = list(f)
    f.close()
    f = open('so.txt','r')
    b=[i.replace("\n", "") for i in f]
    f.close()
    #c=input('Do you want to Display Excel realtime? 1(yes):0(no) defalt:0(NO)?')
    i=10
    while i :
        msg='''
        1 High Speed With Excel Not Show realtime
            System will get the ETD/ETA data from optilo
        2 High Speed With  Show Excel  realtime
            System will get the ETD/ETA data from optilo
        3 Low Speed With Excel Not Show realtime
            System will get the ETD/ETA data from Internet
        4 Low Speed With Show Excel  realtime
            System will get the ETD/ETA data from Internet
        
        
        
        0 exit
        '''
        print(msg)
    #t = threading.Thread(target=close_if_time_pass,args=(5,))
    # start threading
    #t.start()
    # ask him his name
    #ask()

        choice=str(input('>>: '))#.strip()
        if choice == '0':break

        run(a[0],a[1],b,choice)
        break