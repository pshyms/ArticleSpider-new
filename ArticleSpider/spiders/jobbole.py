from scrapy.http import Request
from urllib import parse
import requests
import re
import json
import scrapy

from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils import common


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        """
        parse主要写抓取策略，而不是解析数据
        1. 获取新闻列表页中的新闻url， 并且交给scrapy进行下载后调用后面相应的解析方法
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse继续跟进
        """
        # 获取每一个新闻的url地址
        # url = response.xpath('//*[@id="entry_675040"]/div[2]/h2/a')
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href]').extract_first("")
        # 改写成css方式
        # urls = response.css('#news_list h2 a::attr(href)').extract()

        # 获取所有的新闻节点块,调试的时候可以后面加上[:1]只得到一个节点
        post_nodes = response.css('#news_list .news_block')[1:2]
        for post_node in post_nodes:
            image_url = post_node.css(".entry_summary img::attr(src)").extract_first("")
            post_url = post_node.css(".news_entry a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # 方法1，使用css提取下一页
        # next_url = response.css("div.pager a:last-child::text").extract_first("")
        # if next_url == "Next >":
        #     next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url))

        # 方法2， 使用xpath提取下页，通过文本内容来获取元素
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_url))

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            title = response.css('#news_title a::text').extract_first("")
            create_time = response.css('#news_info .time::text').extract_first("")
            match_time = re.match(".*?(\d+.*)", create_time)
            if match_time:
                create_time = match_time.group(1)
            # 提取文章内容时不要只提取文本，否则会丢失图像等数据。虽然有多余元素，可以后期再分析提取有效元素
            content = response.css('#news_content').extract_first("")
            # 标签可能有多个值，这里先返回列表的形式，然后用join()组合成字符串
            tag_list = response.css('.news_tags a::text').extract()
            tags = ",".join(tag_list)
            # 评论数，阅读数是由js实现的，需要点开network选项卡刷新后查找哪个js发起的哪个请求包含这些数据
            post_id = match_re.group(1)

            # 使用items来传递数据
            articleItem = JobBoleArticleItem()
            articleItem['title'] = title
            articleItem['create_time'] = create_time
            articleItem['tags'] = tags
            articleItem['content'] = content
            # 获得当前页面的url，直接用response.url
            articleItem['url'] = response.url
            # 从parse()中得到传递来的字典数据, 图片的地址需要转为列表，否则会报错
            # 如果没有图片，那么值为[""], 会报错。可以做个判断，如果为空，值为[]
            # if response.meta.get("front_image_url"):
            #     articleItem['front_image_url'] = response.meta.get("front_image_url")
            #     """
            #     https://blog.csdn.net/zhaohaibo_/article/details/104460090
            #     debug时发现,图片URL地址前面以//开头，没有http或者https，会报下面错误
            #     ValueError: Missing scheme in request url: //images0.cnblogs.com/news_topic/ITblog.jpg
            #     所以做个判断，加上https
            #     """
            #     if re.match("^(//).*", articleItem['front_image_url']):
            #         articleItem['front_image_url'] = "https:" + articleItem['front_image_url']
            #     articleItem['front_image_url'] = [articleItem['front_image_url']]
            # else:
            #     articleItem['front_image_url'] = []

            # https://blog.csdn.net/zhaohaibo_/article/details/104460090, 直接使用链接中的方法更简单
            front_image = response.meta.get("front_image_url", "")
            if re.match("^(//).*", front_image):
                front_image = "https:" + front_image
            articleItem["front_image_url"] = [front_image]  # pipeline下载图片一定要传list

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"article_item": articleItem}, callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        praise_num = j_data["DiggCount"]
        fav_num = j_data["TotalView"]
        comment_num = j_data["CommentCount"]

        # 从parse_detail中得到传递来的article_item字典数据
        article_item = response.meta.get("article_item", "")

        # 对上面三个变量进行赋值
        article_item["praise_num"] = praise_num
        article_item["fav_num"] = fav_num
        article_item['comment_num'] = comment_num
        # 根据自定义函数得到URL的MD5值
        article_item['url_object_id'] = common.get_md5(article_item['url'])

        yield article_item   # 会跳转到pipelines，来决定是数据入库还是做进一步的处理
        """
        这里说明两个settings.py中的设置
        1. ROBOTSTXT_OBEY = True   把它改为False
        有些网站中会自定义机器协议，定义一些数据不能被爬取。如果我们设置遵守这个协议，可能造成爬取失败
        可以在域名后加上/robots.txt来查看有哪些限制，比如cnblogs.com/robots.txt
        2. 取消pipeline的注释
        ITEM_PIPELINES = {
        'ArticleSpider.pipelines.ArticlespiderPipeline': 300,
        }
        """






