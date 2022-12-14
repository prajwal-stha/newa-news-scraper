import scrapy,csv


class NewaOnlineNewsScraperSpider(scrapy.Spider):
    name = "newa_news"
    custom_settings = dict(LOG_ENABLED = False)


    start_urls = [
        f"https://www.newaonlinenews.com/news/%E0%A4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF"
        f"%E0%A4%AF?page={i} " for i in range(18)
    ]
    def __init__(self):
        self.outfile = open("newaonlinenews.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news',"additional_info"])

    def close(self, reason):
        self.outfile.close()

    def parse(self, response, **kwargs):
        for link in response.xpath("(//div[@class='view-content'])[2]//ul//li//h4//a/@href").extract():
            yield scrapy.Request(url="https://www.newaonlinenews.com/" + link,
                                 callback=self.get_news)

    def get_news(self, response):

        headline = response.xpath("//div[@class='inner-news-title']//h2//text()").extract()
        additional_info = response.xpath("(//div[@class='cms-content']//p)[1]//text()").extract()
        final_news = []
        for news in response.xpath("//div[@class='cms-content']//p[not(position()=1) and not(position()=last("
                                   "))]//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))
        self.writer.writerow([" ".join(headline), " ".join(final_news)," ".join(additional_info)])
        yield {'headline': " ".join(headline), 'final_news': " ".join(final_news),"additional_info":" ".join(additional_info)}




