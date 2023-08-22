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


url ='https://www.qcc.com/web/search?key=黑龙江仁芯医院'

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

driver2.get(url)