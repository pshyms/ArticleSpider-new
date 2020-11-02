# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # url的MD5处理
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_num = scrapy.Field()
    fav_num = scrapy.Field()
    comment_num = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()