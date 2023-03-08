# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewsPipeline:
    def process_item(self, item, spider):
        return item


import csv
import os


class CategoryCsvPipeline:
    def __init__(self):
        self.files = {}

    def process_item(self, item, spider):
        category = item.get('category')
        if category not in self.files:
            # Create a new CSV file for this category
            filename = f'{category}.csv'
            if os.path.exists(filename):
                mode = 'a'
            else:
                mode = 'w'
            file = open(filename, mode, newline='')
            writer = csv.DictWriter(file, fieldnames=["url", 'category', 'date_published', 'headline', 'news_text'])
            if mode == 'w':
                writer.writeheader()
            self.files[category] = {
                'file': file,
                'writer': writer,
            }
        # Append the news article to the appropriate CSV file
        self.files[category]['writer'].writerow(item)
        return item

    def close_spider(self, spider):
        # Close all the CSV files
        for category in self.files:
            self.files[category]['file'].close()
