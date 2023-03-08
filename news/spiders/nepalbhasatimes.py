import os

import scrapy, csv
import urllib


class NepalBhasaTimesNationalNewsScraperSpider(scrapy.Spider):
    name = 'nepal_bhasa_nepali'
    custom_settings = dict(LOG_ENABLED=False)
    start_urls = [
        f"https://nepalbhasatimes.com/category/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%B0%E0%A4%BE%E0%A4%B" \
        f"7%E0%A5%8D%E0%A4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF/page/{i}" for i in range(0, 954)]

    def __init__(self):
        self.outfile = open("../csv/nepal_bhasa.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news', "date"])

    def parse(self, response, *args, **kwargs):
        for news_links in response.xpath("//a[@class='read-more']/@href").extract():
            yield scrapy.Request(url=news_links, callback=self.get_news)

    def get_news(self, response):
        date_published = response.xpath("(//div[@class='post-single-info']//li//a)[2]//text()").extract_first()
        headline = response.xpath("//div[@class='container']//h1//text()").extract_first()
        final_news = []
        for news in response.xpath("//div[@class='blog-single-details']//p//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))
        self.writer.writerow([headline, " ".join(final_news), date_published])
        yield {'headline': headline, 'final_news': " ".join(final_news),
               "date": date_published}


#
class NepalBhasaTimesForeignNewsScraperSpider(scrapy.Spider):
    name = 'nepal_bhasa_foreign'
    custom_settings = dict(LOG_ENABLED=False)
    start_urls = [
        f"https://nepalbhasatimes.com/category/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%85%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A4%B0%E0%A5%8D%E0%A"
        f"4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF/page/0{i}" for i in
        range(0, 164)]

    def __init__(self):
        self.outfile = open("../csv/nepal_bhasa_foreign_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news', "date"])

    def parse(self, response, *args, **kwargs):
        for news_links in response.xpath("//a[@class='read-more']/@href").extract():
            yield scrapy.Request(url=news_links, callback=self.get_news)

    def get_news(self, response):
        date_published = response.xpath("(//div[@class='post-single-info']//li//a)[2]//text()").extract_first()
        headline = response.xpath("//div[@class='container']//h1//text()").extract_first()
        final_news = []
        for news in response.xpath("//div[@class='blog-single-details']//p//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))
        self.writer.writerow([headline, " ".join(final_news), date_published])
        yield {'headline': headline, 'final_news': " ".join(final_news),
               "date": date_published}


class NepalBhasaTimesScraperSpider(scrapy.Spider):
    name = 'nepal_bhasa'
    custom_settings = {"LOG_ENABLED": False, 'ITEM_PIPELINES': {'news.pipelines.CategoryCsvPipeline': 400}}
    start_urls = ["https://nepalbhasatimes.com/"]

    def parse(self, response, *args, **kwargs):
        links = response.xpath("(//ul[@id='menu-newa-menu']//a)[position() > 2 and position() < last()-3]")
        for link in links:
            href = link.attrib['href']
            if href != "#" and href is not None:
                text = link.xpath('text()').get().strip()
                yield scrapy.Request(url=href, callback=self.get_news_category, meta={"text": text})

    def get_news_category(self, response):
        """
        used to get each category url and pagination size
        :param response:
        :return:
        """
        category = response.meta.get('text')
        pagination_size = int(
            response.xpath("/html/body/div[2]/section[2]/div/div/div/div/nav/ul/li[5]/a/text()").get())

        for number in range(1, pagination_size):
            yield scrapy.Request(url=response.url + f"/page{number}", callback=self.get_news,
                                 meta={"category": category})

    def get_news(self, response):
        category = response.meta.get('category')
        for news_links in response.xpath("//a[@class='read-more']/@href").extract():
            yield scrapy.Request(url=news_links, callback=self.get_actual_news, meta=dict(category=category))

    def get_actual_news(self, response):
        self.category = response.meta.get('category')
        date_published = response.xpath("(//div[@class='post-single-info']//li//a)[2]//text()").extract_first()
        headline = response.xpath("//div[@class='container']//h1//text()").extract_first()
        final_news = []

        if headline and date_published:
            for news in response.xpath("//div[@class='blog-single-details']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))

        yield {
            "url": response.url,
            'category': self.category,
            'date_published': date_published,
            'headline': headline,
            'news_text': " ".join(final_news),
        }
