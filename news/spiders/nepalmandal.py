import csv
import os

import scrapy


class NepalMandal(scrapy.Spider):
    name = 'nepalmandal'
    start_urls = [f"http://www.nepalmandal.com/cat/59/{i}.html" for i in range(0, 25)]
    custom_settings = dict(LOG_ENABLED=False)
    def __init__(self):
        self.outfile = open("nepal_mandal/मू बुखँ.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'date', 'final_news','url'])

    def parse(self, response, **kwargs):
        for links in response.xpath("//div[@class='post']//a[@class='nepali']/@href").extract():
            yield scrapy.Request(
                url=f"http://www.nepalmandal.com/{links}",
                callback=self.get_full_news)

    def get_full_news(self, response):
        headline = response.xpath("//div[@class='post']//h1/text()").extract()[0]
        posted_on = response.xpath("//div[@class='byline']//div//small/text()").extract()[0]
        # for news in response.xpath("//div[@class='entry']//p/text()").extract():
        cleaned_list = [x.strip() for x in response.xpath("//div[@class='entry']//p/text()").extract() if x.strip()]
        final_news = " ".join(cleaned_list)
        self.writer.writerow([headline, posted_on,final_news,response.url ])

