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
from selenium.webdriver.support.select import Select
def run():
    ch_options = Options()
    #ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #prefs = {'download.default_directory': base_path,'profile.default_content_settings.popups': 0}
    #ch_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 

    #driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    driver.maximize_window() 
    url ='https://nlyehvdcs3vw102.code1.emi.philips.com/ComOps/PCR_tool/PCRAlert.aspx'
    driver.headers = {  
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
            }  
    driver.get(url)
    time.sleep(1) 
    link=driver.find_element_by_xpath('//*[@id="User"]') 
    link.send_keys('lucy.yang@philips.com')#'sylar.sun@philips.com'
    user=driver.find_element_by_xpath('//*[@id="PassWord"]')
    user.send_keys('Lucy5118///')#'a8my4pai'

    cmd=driver.find_element_by_xpath('//*[@id="logMeIn"]')
    cmd.click()

    time.sleep(1) 
    #summary
    
    s = driver.find_element_by_name("Alert_Name1")
    Select(s).select_by_visible_text("BOOKING_HORIZON")
    Select(s).select_by_visible_text("CAD_NOT_FILLED")
    Select(s).select_by_visible_text("CREATE_AFTER_FNBL")
    Select(s).select_by_visible_text("FNBL_BUT_NOT_INVCD")
    Select(s).select_by_visible_text("GI_OVERDUE")
    Select(s).select_by_visible_text("GR_TOO_LATE")
    Select(s).select_by_visible_text("NO_CLEAN_ORDER_CODE")
    Select(s).select_by_visible_text("NO_WBS_FILLED")
    Select(s).select_by_visible_text("ORDERS_HAVE_Y9")
    Select(s).select_by_visible_text("RDD_QUALITY")
    Select(s).select_by_visible_text("RECOGNITION_DATES")
    Select(s).select_by_visible_text("RETURN_NOT_COMPLTD")
    try: Select(s).select_by_visible_text("S67_IS_UNDIVIDED")
    except:         pass
    Select(s).select_by_visible_text("STAND_ALONE_PO")
    Select(s).select_by_visible_text("ZPO_ZSO_FUNLOC")


    s = driver.find_element_by_name("Order_Admin")
    try: Select(s).select_by_visible_text("320108431")
    except:         pass
    try: Select(s).select_by_visible_text("320114093")
    except:         pass
    try: Select(s).select_by_visible_text("320114553")
    except:         pass
    try: Select(s).select_by_visible_text("320127178")
    except:         pass
    try: Select(s).select_by_visible_text("320133063")
    except:         pass
    try: Select(s).select_by_visible_text("320157646")
    except:         pass
    try: Select(s).select_by_visible_text("An Sundance")
    except:         pass
    try: Select(s).select_by_visible_text("Chen Jade")
    except:         pass
    try: Select(s).select_by_visible_text("Chen Yiying")
    except:         pass
    try: Select(s).select_by_visible_text("Cui Nicole")
    except:         pass
    try: Select(s).select_by_visible_text("Ishihara Akemi")
    except:         pass
    try: Select(s).select_by_visible_text("Ishihara Makiko")
    except:         pass
    try: Select(s).select_by_visible_text("Ito Emi")
    except:         pass
    try: Select(s).select_by_visible_text("Kanamaru Mariko")
    except:         pass
    try: Select(s).select_by_visible_text("Kim Euncheol")
    except:         pass
    try: Select(s).select_by_visible_text("Li Helen")
    except:         pass
    try: Select(s).select_by_visible_text("Li Shu Ting")
    except:         pass
    try: Select(s).select_by_visible_text("Li Suna")
    except:         pass
    try: Select(s).select_by_visible_text("Liao Lisa")
    except:         pass
    try: Select(s).select_by_visible_text("Ling Yi")
    except:         pass
    try: Select(s).select_by_visible_text("Lucy Yang")
    except:         pass
    try: Select(s).select_by_visible_text("Ma Yi Fei")
    except:         pass
    try: Select(s).select_by_visible_text("Morisaki Reina")
    except:         pass
    try: Select(s).select_by_visible_text("Qin Qian Ru")
    except:         pass
    try: Select(s).select_by_visible_text("Sakai Tomoe")
    except:         pass
    try: Select(s).select_by_visible_text("Shi Yuye")
    except:         pass
    try: Select(s).select_by_visible_text("Sun Bing Jie")
    except:         pass
    try: Select(s).select_by_visible_text("Wu Xue Qiong")
    except:         pass
    try: Select(s).select_by_visible_text("Xie Shirley")
    except:         pass
    try: Select(s).select_by_visible_text("Xu Anna")
    except:         pass
    try: Select(s).select_by_visible_text("Xu Hsinwen")
    except:         pass
    try: Select(s).select_by_visible_text("Yagi Hirokazu")
    except:         pass
    try: Select(s).select_by_visible_text("Yamakami Mizue")
    except:         pass
    try: Select(s).select_by_visible_text("Yu Jian Ya")
    except:         pass
    try: Select(s).select_by_visible_text("Zhang Li")
    except:         pass
    try: Select(s).select_by_visible_text("Zhang Nicole")
    except:         pass
    try: Select(s).select_by_visible_text("Zhang Zoe")
    except:         pass
    try: Select(s).select_by_visible_text("Zhu Doris")
    except:         pass

    try: Select(s).select_by_visible_text("320069979")
    except:         pass
    try: Select(s).select_by_visible_text("Rachel Yu")
    except:         pass
    try: Select(s).select_by_visible_text("320179478")
    except:         pass
    try: Select(s).select_by_visible_text("Xinfang Lee")
    except:         pass
    try: Select(s).select_by_visible_text("320184671")
    except:         pass
    try: Select(s).select_by_visible_text("Wen Yang")
    except:         pass
    try: Select(s).select_by_visible_text("320070349")
    except:         pass
    try: Select(s).select_by_visible_text("320126252")
    except:         pass
    try: Select(s).select_by_visible_text("Chen Yiying")
    except:         pass
    try: Select(s).select_by_visible_text("320161250")
    except:         pass
    try: Select(s).select_by_visible_text("Lu Erin")
    except:         pass
    
    s = driver.find_element_by_name("VALUE_STREAM")
    Select(s).select_by_visible_text("GBS Suzhou Japan")

    s = driver.find_element_by_name("Sales_Org")
    Select(s).select_by_visible_text("JP90")




    cmd=driver.find_element_by_xpath('//*[@id="GET_ORDERS"]')
    cmd.click()
    time.sleep(25) 
    #cmd=driver.find_element_by_xpath('//*[@id="imgLoading"]')
    cmd=driver.find_element_by_xpath('//*[@id="imgExportExcel"]')
    cmd.click()

    link=driver.find_element_by_xpath('//*[@id="User"]') 



if __name__=='__main__':    
    run()