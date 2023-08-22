from sqlite3 import dbapi2
from selenium import webdriver
import time
import json
import shutil
import os,sys
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
global aa,ab,ac,ad

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

def findritong2(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    ac=aa=ab=ad=""
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 在启动浏览器时加入配置
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.maximize_window() 
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver2.get('https://shuttle.nipponexpress.com/shuttle_service/generalTrackingSearch')
    
    X=driver2.find_element_by_xpath('//*[@id="search"]/table/tbody/tr[2]/td[1]/input')
    X.send_keys(url2)

    search=driver2.find_element_by_xpath('//*[@id="button"]/button/img')
    search.click()
    ac=driver2.find_element_by_xpath('//*[@id="detail1"]/div/table/tbody/tr[2]/td[1]').text
    ad=driver2.find_element_by_xpath('//*[@id="detail1"]/div/table/tbody/tr[2]/td[3]').text
    aa=driver2.find_element_by_xpath('//*[@id="detail1"]/div/table/tbody/tr[3]/td[1]').text
    ab=driver2.find_element_by_xpath('//*[@id="detail1"]/div/table/tbody/tr[3]/td[3]').text

    driver2.quit()
    return(ac,ad,aa,ab)

def findritong(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    ac=aa=ab=ad=""
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

    ac=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/span').text
    ad=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div[2]/span').text
    aa=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[2]/span').text
    ab=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div[2]/span').text

    driver2.quit()
    return(ac,ad,aa,ab)
    

def findfrex(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    #ac=aa=ab=ad=""
    ch_options = Options()
    #ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #ch_options.add_experimental_option('excludeSwitches', ['enable-automation']) #使用chrome开发者模式
    
    ch_options.add_argument('--disable-blink-features=AutomationControlled')#禁用启用Blink运行时的功能
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            } 
    driver2.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                    })
                """
    })#Selenium执行cdp命令 再次覆盖window.navigator.webdriver的值
    driver2.maximize_window()  
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver2.get(url2)
    #time.sleep(4)
    WebDriverWait(driver2,10).until(lambda x: x.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]'))
    
    ac=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]').text
    
    ad=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[2]').text
    
    aa=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[1]').text
    
    ab=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[2]/span').text
    
    driver2.quit()
    return(aa,ab,ac,ad)

    

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
    excel=win32.DispatchEx('Excel.Application')
    excel.Visible = dis
    #twb=excel.Workbooks.Open(rfile)
    twb=excel.Workbooks.Add()
    tsheet=twb.Worksheets(1)
    head=["PO","Carrier main reference","ETD D","ETD A","ETA D","ETA A","ZTO NO","Meatil","QTY","Name","Company","pack list","trace list","salse invoice"]
    
    tsheet.Range("A1:N1").Value=head
    #poall=['4516844107','4517056354','4516731849','4516426656','4517186111','4517119035','4516898288','4517098439','4516578434','4516790660','4516731841','4517063191','4516750588','4516894131']
    #poall=['4516586853','4516780830','4517098306','4516628159','4517098976','4516995041']
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
    #driver = webdriver.Chrome()
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
    user.send_keys(pwd)#'a8my4pai'

    cmd=driver.find_element_by_xpath('//*[@id="submitLogin"]')
    cmd.click()

    time.sleep(1) 
    #summary
    #driver.find_element_by_xpath('//*[@id="menu-1-163995"]/a').click()
    driver.find_element_by_link_text("Summary").click()
    WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']"))

    for  pon in poall:
        po=driver.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']")
        #po=driver.find_element_by_xpath('//*[@id="DF100007367_mp1_so_number"]')
        driver.execute_script("arguments[0].value = '" + pon + "';", po)
        #po.send_keys(pon)#4516773895

        driver.find_element_by_xpath('//*[@id="content_6f962c95b57247a66951fd7a883e2c27"]/div[2]/div/input[1]').click()

        time.sleep(1) 

        #try:
        data1=driver.find_element_by_xpath('//*[@id="content_0a3ddf58e49fb088dc15a424277fd953"]')
        if data1.text=="No data":
            tsheet.Range("A"+str(rowi)).Value=pon
            tsheet.Range("B"+str(rowi)).Value="No data in optilo"
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
            #tsheet.cells(rowi,1).Value=pon
            tsheet.Range("A"+str(rowi)).Value=pon

            for i in range(2,a_trn+1): #行
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[6]')
                tsheet.Range("J"+str(rowi)).Value=x.text
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]')
                tsheet.Range("O"+str(rowi)).Value=x.text
                if x.text[0:3]=='MJB':                    
                    if len(x.text)<11:
                        y =driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]/a[1]')
                    else:
                        y =driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]/a')
                    tsheet.Range("A"+str(rowi)).Value=pon
                    y.click()
                    time.sleep(1)
                    driver.switch_to.frame(0) 
                    try:
                        m=driver.find_element_by_xpath('//*[@id="DF650000163_carrier_id_krt_kontrahent_assigned"]')
                        tsheet.Range("K"+str(rowi)).Value=m.get_attribute("value")
                        if m.get_attribute("value")[0:5]=="Fedex":
                            s=driver.find_element_by_xpath('//*[@id="DF650000229_carrier_reference1"]')
                            sno=s.get_attribute("value")
                            tsheet.Range("B"+str(rowi)).Value="'" + sno
                            #url2='https://www.fedex.com/fedextrack/?tracknumbers=' + sno + '&cntry_code=jp'
                            #wuliu=findfrex(url2)
                            # for q in range(4):
                            #         tsheet.cells(rowi,q+3).Value=wuliu[q]  
                            #tsheet.Range("C"+str(rowi)+":F"+str(rowi)).Value=wuliu
                        if m.get_attribute("value")[0:6]=="Nippon":    
                            m=driver.find_element_by_xpath('//*[@id="DF650000229_air_mawb_no"]')
                            #print(m.get_attribute("value"))
                            n=m.get_attribute("value")
                            if len(n)>1:
                                tsheet.Range("B"+str(rowi)).Value=n
                                # if n.find("-")>=0: 
                                #     url2='https://www.nca.aero/icargoportal/portal/trackshipments?&trkTxnValue=' + n
                                # else:
                                #     url2='https://www.nca.aero/icargoportal/portal/trackshipments?&trkTxnValue=' + n[0:3]+'-'+n[3:11]
                                #wuliu=findritong2(n)
                                #tsheet.Range("C"+str(rowi)+":F"+str(rowi)).Value=wuliu
      
                    except:
                        pass
                    finally:
                        driver.switch_to.default_content()
                        driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()

                time.sleep(1)
                try:
                    driver.switch_to.frame(0)
                except:
                    pass
                x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[2]')
                tsheet.Range("G"+str(rowi)).Value=x.text
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
                for i in range(2,trn+1): #行
                    #check file is pdf
                    file1=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[2]')
                    if file1.text[-3:]=='pdf':
                        m=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[2]/a')
                        n=driver.find_element_by_xpath('//*[@id="DP690000322"]/tbody/tr[' + str(i) + ']/td[5]')
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
                        isExists=os.path.exists('Y:\\logsic\\' + tsheet.Range("G"+str(rowi)).Value )
                        if not isExists:
                            os.makedirs('Y:\\logsic\\' +tsheet.Range("G"+str(rowi)).Value)         
                        newname = 'Y:\\logsic\\' +tsheet.Range("G"+str(rowi)).Value + "\\" + n.text.split(' ')[0]+"."+file_type
                        #os.rename(oldname, newname)
                        shutil.move(oldname, newname)
                        #print('归档成功')"""
                        if n.text.split(' ')[0]=='trace':
                            tsheet.Range("L"+str(rowi)).Value="Y"
                        else:
                            if n.text.split(' ')[0]=='pack':
                                tsheet.Range("M"+str(rowi)).Value="Y"
                            else:
                                if n.text.split(' ')[0]=='sales':
                                    tsheet.Range("N"+str(rowi)).Value="Y"
                #end files

                #begin order lines
                #time.sleep(1) #why don't click
                WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath('//*[@id="mytabs0"]/ul/li[2]/a/span')).click()
                trlist = driver.find_elements_by_xpath('//*[@id="DG690000215"]/tbody/tr') #行
                tdlist = driver.find_elements_by_xpath('//*[@id="DG690000215"]/tbody/tr/td') #列

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
                for i in range(2,trn+1): #行
                    m=driver.find_element_by_xpath('//*[@id="DG690000215"]/tbody/tr[' + str(i) + ']/td[5]')
                    n=driver.find_element_by_xpath('//*[@id="DG690000215"]/tbody/tr[' + str(i) + ']/td[7]')
                    tsheet.Range("H"+str(rowi)).Value="'" + str(m.text)
                    tsheet.Range("I"+str(rowi)).Value=n.text[0:len(n.text)-5]
                    rowi=rowi+1
                #end order lines

                try:
                    driver.switch_to.default_content()
                except:
                    pass
                driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()
                driver.switch_to.default_content()
        # except:
        #     rowi=rowi+1
        # finally:
        #     pass

    driver.quit()
    excel.Visible = 1

if __name__=='__main__':
    ac=aa=ab=ad=""    
    f = open('1.txt','r')
    a = list(f)
    f.close()
    f = open('po.txt','r')
    b=[i.replace("\n", "") for i in f]
    f.close()
    c=input('Do you want to Display Excel realtime? 1(yes):0(no) defalt:0(NO)?')
    if c=='1':
        run(a[0],a[1],b,1)
    else:
        run(a[0],a[1],b)
