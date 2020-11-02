# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        # 这里设置断点，可以看到jobbole.py中定义的各字段的值
        return item
