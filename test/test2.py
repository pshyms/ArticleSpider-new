# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['oursteps.com.au']
    # 这个默认的起点网址可以不用，因为我们下面配置了start-requests的方法，他们的功能类似，都是去爬第一个起始的网址
    # start_urls = ['http://oursteps.com.au/']
    # 这个header可以是任何浏览器的头文件，用于伪装
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    # 里面的查询地址最好是使用在fidder里面看见的地址，cookiejar设为真，parse是用一个回调函数，执行爬取信息之后对应的操作
    def start_requests(self):
        return [Request("http://www.oursteps.com.au/", meta={"cookiejar": 1}, callback=self.parse)]

    # 发送一个post请求，数据是字典格式的，发送完了之后执行另外一个回调函数
    def parse(self, response):
        data = {
            "username": "pshyms",
            "password": "Shiyan823",
        }

        print("ready to login")
        # 通过FormRequest.from_response()进行登陆
        return [FormRequest.from_response(response,
                                          # 设置cookie信息
                                          meta={"cookiejar": response.meta["cookiejar"]},
                                          # 设置headers信息模拟成浏览器
                                          headers=self.header,
                                          # 设置post表单中的数据
                                          formdata=data,
                                          # 设置回调函数，此时回调函数为next()
                                          callback=self.next,
                                          )]

# 回调函数，直接把返回的页面保存下来
    def next(self,response):
        data=response.body
        # 注意是二进制格式
        f = open("D:/temp/ourstep/a.html", "wb")
        f.write(data)
        f.close()
# 登录成功了之后，再跳转到另外一个页面去，记住带着cookie的状态
        yield Request("http://www.oursteps.com.au/bbs/portal.php?mod=article&aid=82186", callback=self.next2,meta={"cookiejar": True})

# 保存新页面的内容
    def next2(self, response):
        data = response.body
        f = open("D:/temp/ourstep/b.html", "wb")
        f.write(data)
        f.close()