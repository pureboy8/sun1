from selenium import webdriver
import time
import json
import shutil
import os,sys
from win32com.client import constants
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
# import pandas as pd
# import numpy as np
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

    ac=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div[2]/span').text
    #tsheet.cells(rowi,3).Value=ac.text
    ad=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div[2]/span').text
    #tsheet.cells(rowi,4).Value=ad.text
    aa=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[2]/span').text
    #tsheet.cells(rowi,5).Value=nc.text
    ab=driver2.find_element_by_xpath('//*[@id="' + no_ship + '"]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div[2]/div[2]/span').text
    #tsheet.cells(rowi,6).Value=nd.text
    #twb.SaveAs(targetfile)

    driver2.quit()
    return(ac,ad,aa,ab)
    

def findfrex(url2):
    #driver2 = webdriver.PhantomJS()
    #driver2 = webdriver.Chrome()
    ch_options = Options()
    #ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    #ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 在启动浏览器时加入配置
    driver2 = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    driver2.maximize_window() 
    driver2.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }
    driver2.get_cookies()          
    driver2.get(url2)
    #time.sleep(4)
    WebDriverWait(driver2,10).until(lambda x: x.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]'))
    
    ac=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[1]').text
    
    ad=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[2]').text
    
    aa=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-text/div/h3[1]').text
    
    ab=driver2.find_element_by_xpath('//*[@id="container"]/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/trk-shared-shipment-status-delivery-date/h1/span[2]/span').text
    

    driver2.quit()
    return(ac,ad,aa,ab)

    

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

def run(usr,pwd,dis=0):
    #excel=win32.DispatchEx('Excel.Application')
    excel=win32.gencache.EnsureDispatch('Excel.Application')
    excel.Visible = dis
    twb=excel.Workbooks.Open(r'c:\work\temp\BO(FDCSIB).xlsx')
    # twb=excel.Workbooks.Add()
    tsheet=twb.Worksheets(1)
    poall=[]

    global base_path
    base_path=r'C:\work\temp'
    profile = {
        'download.default_directory': base_path
        }

    ch_options = Options()
    #ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {'download.default_directory': base_path,'profile.default_content_settings.popups': 0}
    ch_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
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
    #driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    for row in range(2,tsheet.Range("A65536").End(constants.xlUp).Row+1):
        if tsheet.Range('L'+str(row)).Value == "◎":
            pon=str(int(tsheet.Range('H'+str(row)).Value))
            WebDriverWait(driver,10).until(lambda x: x.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']"))
            po=driver.find_element_by_xpath("//*[@id='DF100007367_purchase_order_number']")
            #po=driver.find_element_by_xpath('//*[@id="DF100007367_mp1_so_number"]')
            driver.execute_script("arguments[0].value = '" + pon + "';", po)
            #po.send_keys(pon)#4516773895

            driver.find_element_by_xpath('//*[@id="content_6f962c95b57247a66951fd7a883e2c27"]/div[2]/div/input[1]').click()

            time.sleep(1) 

 
            data1=driver.find_element_by_xpath('//*[@id="content_0a3ddf58e49fb088dc15a424277fd953"]')
            if data1.text=="No data":
                tsheet.Range('K'+str(row)).Value="No data in optilo"
                
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
                

                for i in range(2,a_trn+1): #行
                    z= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[6]').text
                    x= driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]').text
                    if x[0:3]=='MJB' and z[0:12]=='459800424141':
                        if len(x)<11:
                            y =driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]/a[1]')
                        else:
                            y =driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[4]/a')
                        y.click()
                        time.sleep(1)
                        driver.switch_to.frame(0) 
                        try:
                            m=driver.find_element_by_xpath('//*[@id="DF650000163_carrier_id_krt_kontrahent_assigned"]')
                            tsheet.Range('K'+str(row)).Value=driver.find_element_by_xpath('//*[@id="DF650000163_end_real_datetime"]').get_attribute("value")
                            tsheet.Range('J'+str(row)).Value=driver.find_element_by_xpath('//*[@id="DF650000163_start_real_datetime"]').get_attribute("value")
                            print(driver.find_element_by_xpath('//*[@id="DF650000163_start_plan_datetime"]').get_attribute("value"))
                            if m.get_attribute("value")[0:5]=="Fedex" and tsheet.Range('K'+str(row)).Value!="":
                                tsheet.Range('L'+str(row)).Value = "◎"
                            if tsheet.Range('J'+str(row)).Value=="":
                                tsheet.Range('J'+str(row)).Value=driver.find_element_by_xpath('//*[@id="DF650000163_start_plan_datetime"]').get_attribute("value")
                            if tsheet.Range('K'+str(row)).Value=="":
                                tsheet.Range('K'+str(row)).Value=driver.find_element_by_xpath('//*[@id="DF650000163_end_plan_datetime"]').get_attribute("value")

                            if m.get_attribute("value")[0:5]=="Fedex":
                                s=driver.find_element_by_xpath('//*[@id="DF650000229_carrier_reference1"]')
                                sno=s.get_attribute("value")
                                
                                url2='https://www.fedex.com/fedextrack/?tracknumbers=' + sno + '&cntry_code=jp'
                                wuliu=findfrex(url2)
                                for q in range(4):
                                    tsheet.Range('M'+str(row)).Value=wuliu[1]
                            if m.get_attribute("value")[0:6]=="Nippon":    
                                m=driver.find_element_by_xpath('//*[@id="DF650000229_air_mawb_no"]')
                                #print(m.get_attribute("value"))
                                n=m.get_attribute("value")
                                if len(n)>1:
                                    
                                    if n.find("-")>=0: 
                                        url2='https://www.nca.aero/icargoportal/portal/trackshipments?&trkTxnValue=' + n
                                    else:
                                        url2='https://www.nca.aero/icargoportal/portal/trackshipments?&trkTxnValue=' + n[0:3]+'-'+n[3:11]
                                    wuliu=findritong(url2)
                                    for q in range(4):
                                        tsheet.Range('M'+str(row)).Value=wuliu[1]        
                        except:
                            pass
                        finally:
                            driver.switch_to.default_content()
                            driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()


                    try:
                        driver.switch_to.default_content()
                    except:
                        pass
                    #driver.find_element_by_xpath('//*[@id="TB_closeWindowButton"]').click()
                    driver.switch_to.default_content()
        # except:
        #     tsheet.cells(rowi,1).Value=pon
        #     tsheet.cells(rowi,2).Value="No data in optilo"
        #     rowi=rowi+1
        # finally:
        #     pass

    driver.quit()
    twb.Save()
    #excel.Visible = 1
    excel.Quit()

if __name__=='__main__':    
    f = open('1.txt','r')
    a = list(f)
    f.close()
    c=input('Do you want to Display Excel realtime? 1(yes):0(no) defalt:0(NO)?')
    if c=='1':
        run(a[0],a[1],1)
    else:
        run(a[0],a[1])
