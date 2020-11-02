# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class ArticlespiderPipeline:
    def process_item(self, item, spider):
        # 这里设置断点，可以看到jobbole.py中定义的各字段的值
        return item


# 重写一个pipeline，显示已下载图片的本地路径
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:  # 可以在这里打断点查看results, item都有什么值
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item

