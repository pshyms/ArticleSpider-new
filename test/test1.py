# -*- coding: utf-8 -*-
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
data = {
            "UserName": "MMService",
            "PassWord": "MagnetMonitor",
        }
url = 'http://http://192.168.0.1/index_prop.html'
session = requests.Session()
session.post(url, headers=headers, data=data)
# 登录后，我们需要获取另一个网页中的内容
response = session.get('http://192.168.0.1/index_prop.html', headers=headers)
print(response.status_code)
print(response.text)

# f = open("C:/temp/ourstep/c.html", "wb")
# f.write(response.text.encode("utf-8"))
# f.close()


#MagnetMonitor