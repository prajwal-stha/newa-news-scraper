import scrapy,csv


class LahanNewsScraperSpider(scrapy.Spider):
    itemlist = []
    custom_settings = dict(LOG_ENABLED=False)
    name = "lahan_news"
    start_urls = [
        f"https://www.lahananews.com/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A4"
        f"%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page={i}" for i in range(0,524)
    ]

    def __init__(self):
        self.outfile = open("lahan_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news','date'])

    def close(self, reason):
        self.outfile.close()

    def parse(self, response, **kwargs):
        for news_link in response.xpath("//div[@class='hot-news-box']//li//div//h3//a/@href").extract():
            yield scrapy.Request(url="https://www.lahananews.com/" + news_link,
                                 callback=self.get_news)

    def get_news(self, response):
        headline = (response.xpath("//div[@class='news-section-title']//h2//text()").extract())
        date = response.xpath("//div[@class='content']/p//text()").extract()
        final_news = []
        for news in response.xpath("//span[@style='font-size:18px;']//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news)==0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news)>0:
            self.writer.writerow([" ".join(headline)," ".join(final_news)," ".join(date)])
            yield {'headline': " ".join(headline) , 'final_news': " ".join(final_news),"date":" ".join(date)}


class LahanForeignNewsScraperSpider(scrapy.Spider):
    itemlist = []
    custom_settings = dict(LOG_ENABLED=False)
    name = "lahan_foreign_news"
    start_urls = [
        f"https://www.lahananews.com/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%85%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A4%B0%E0%A5%8D%E0%A4%B0%E0%A4%" \
        f"BE%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page=0{i}" for i in range(0,83)
    ]

    def __init__(self):
        self.outfile = open("lahan_foreign_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news','date'])

    def close(self, reason):
        self.outfile.close()

    def parse(self, response, **kwargs):
        for news_link in response.xpath("//div[@class='hot-news-box']//li//div//h3//a/@href").extract():
            yield scrapy.Request(url="https://www.lahananews.com/" + news_link,
                                 callback=self.get_news)

    def get_news(self, response):
        headline = (response.xpath("//div[@class='news-section-title']//h2//text()").extract())
        date = response.xpath("//div[@class='content']/p//text()").extract()
        final_news = []
        for news in response.xpath("//span[@style='font-size:18px;']//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news)==0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news)>0:
            self.writer.writerow([" ".join(headline)," ".join(final_news)," ".join(date)])
            yield {'headline': " ".join(headline) , 'final_news': " ".join(final_news),"date":" ".join(date)}
