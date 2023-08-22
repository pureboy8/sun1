from selenium import webdriver
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import win32com.client as win32

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
    

if __name__=='__main__':    
    a=dsv('UDF0015746')
    print(a)