# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

class ArticlespiderPipeline:
    def process_item(self, item, spider):
        # 这里设置断点，可以看到jobbole.py中定义的各字段的值
        return item


# 重写一个pipeline，显示已下载图片的本地路径,方便保存在数据库中查看
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_file_path = ""
        for ok, value in results:  # 可以在这里打断点查看results, item都有什么值
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item


# 保存item字段内容到本地，并且使用scrapy内部提供的JsonItemExporter来转变为json格式的文件
class JsonExporterPipeline:
    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

