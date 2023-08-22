
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options # => 引入Chrome的配置
def dbs(no):
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # prefs = {'download.default_directory': base_path,'profile.default_content_settings.popups': 0}
    # ch_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    # driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    # driver.maximize_window() 
    url ='https://eschenker.dbschenker.com/nges-portal/api/public/tracking-public/shipments?query=' + no
    driver.headers = {  
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
        }  
    driver.get(url)
    # html=driver.page_source()
    html=driver.find_element_by_xpath('/html/body/pre').text

    dic = json.loads(html)
    driver.quit()
    return '',dic['result'][0]['startDate'],'',dic['result'][0]['endDate'] 
def cos(no):
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # prefs = {'download.default_directory': base_path,'profile.default_content_settings.popups': 0}
    # ch_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    # driver = webdriver.PhantomJS()
    #driver = webdriver.Chrome()
    # driver.maximize_window() 
    url ='https://elines.coscoshipping.com/ebtracking/public/bill/' + no
    driver.headers = {  
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
        }  
    driver.get(url)
    # html=driver.page_source()
    html=driver.find_element_by_xpath('/html/body/pre').text

    dic = json.loads(html)
    driver.quit()
    return dic['data']['content']['actualShipment'][0]['expectedDateOfDeparture'],dic['data']['content']['actualShipment'][0]['expectedDateOfDeparture'],dic['data']['content']['actualShipment'][0]['estimatedDateOfArrival'],dic['data']['content']['actualShipment'][0]['actualArrivalDate'] 
    #return ,dic['data']['content']['actualDepartureDate']['expectedDateOfDeparture'],dic['data']['content']['actualShipment']['estimatedDateOfArrival'],dic['data']['content']['actualShipment']['actualArrivalDate'] 
def exp(no):
    ch_options = Options()
    ch_options.add_argument("--headless")  # => 为Chrome配置无头模式
    ch_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=ch_options) # => 注意这里的参数 
    url ='http://expo.expeditors.com/expo/SQGuest?SearchType=shipmentSearch&TrackingNumber=4030462233'# + no
    url='http://expo.expeditors.com/expo/SQGuest?SearchType=eventsSearch&reference=4030462233'
    driver.headers = {  
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"  
        }  
    driver.get(url)
    html=driver.find_element_by_xpath('/html/body').text
    #print(html)
    table_ele = driver.find_elements_by_xpath('//*[@id="sqgDetailEventsTabTable"]')[0] #定位到table 
    rows = table_ele.find_elements_by_tag_name("tr")   #定位table下的tr标签
    #html=driver.find_element_by_xpath('/html/body/pre').text
    numbers = len(rows)  
    # print(type(numbers)) # 打印类型，输入为int
    # print(numbers) #打印行数
    app_name_list=[]  #定义数组来存取遍历得到的应用名称值
    #driver.find_element_by_xpath('//*[@id="DL100007368"]/tbody/tr[' + str(i) + ']/td[6]')
    for i in range(numbers-1):
        for j in  range(5):
            x=driver.find_element_by_xpath('//*[@id="sqgDetailEventsTabTable"]/tbody/tr[' + str(i+1) + ']/td['+ str(j+1) +']').text
            print(x,end=",")
        print()

        # i 默认从0开始，而定位元素是从1开始，所以需i+1
        # i 是int类型，元素定位中的tr[i] 是string 类型，所以需进行类型转换
        # 使用str()将int转换为String
        # 此元素定位是获取表格中的应用名称的值，需注意后面的text
    #     app_names = driver.find_elements_by_xpath('//*[@id="sqgDetailEventsTabTable"][1]//tr[' + str(i+1) + ']//td[3]//div')[0].text
    #     app_name_list.append(app_names)  #遍历一次，就加入数组中
    # print(app_name_list) #打印出遍历完成的数组
    driver.quit()
    #dic = json.loads(html)
if __name__=='__main__':
    #print(dbs('AMS88207263'))
    #print(cos('5156551530'))
    exp('a')

# time.sleep(3) 
# head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

# data = requests.get(url=url,headers=head).text
# print(data)