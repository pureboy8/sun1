# 打开网站www.baidu.com，将结果保存在txt文件中

import requests
url = 'http://www.baidu.com'

try:
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    with open('baidu.txt','w',encoding='utf-8') as f:
        f.write(r.text)
        print('俩存成功')
        
except:
    print('爬取失败')

   
    