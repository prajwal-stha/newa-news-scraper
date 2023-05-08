# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class NewsPipeline:
    def process_item(self, item, spider):
        return item


import csv
import os

from scrapy.exceptions import DropItem


class CategoryCsvPipeline:
    def __init__(self):
        self.files = {}

    def process_item(self, item, spider):
        category = item.get('category')
        if category is None:
            raise DropItem("Category is not defined for item")
        folder_name = 'nepal_bhasa_csv_files'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        filename = f'{folder_name}/{category}.csv'
        if category not in self.files:
            # Create a new CSV file for this category
            mode = 'a' if os.path.exists(filename) else 'w'
            file = open(filename, mode, newline='')
            writer = csv.DictWriter(file, fieldnames=["url", 'category', 'author', 'date', 'date_published', 'headline',
                                                      'news_text'])
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


class LahanNewsCategoryCsvPipeline:
    def __init__(self):
        self.files = {}

    def process_item(self, item, spider):
        category = item.get('category')
        if category is None:
            raise DropItem("Category is not defined for item")
        folder_name = 'lahan_news_csv_files'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        if category == 'च्वसु/बिचा:':
            category = category.split('/')[0]
        filename = f'{folder_name}/{category}.csv'
        if category not in self.files:
            # Create a new CSV file for this category
            mode = 'a' if os.path.exists(filename) else 'w'
            file = open(filename, mode, newline='')
            writer = csv.DictWriter(file, fieldnames=['category', 'author', 'date', 'headline', 'final_news', "url"])
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
