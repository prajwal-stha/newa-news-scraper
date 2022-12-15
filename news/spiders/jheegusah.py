import scrapy,csv


class JheegushaNewsScraperSpider(scrapy.Spider):
    name = "jheegu_news"
    start_urls = [f"https://jheegusah.com/news/%E0%A4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A"
                  f"4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page={i}" for i in range(0,7)]

    def __init__(self):
        self.outfile = open("../csv/jheegu_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news',"date"])

    def close(self, reason):
        self.outfile.close()

    def parse(self, response, **kwargs):
        for news_link in response.xpath("//ul[@class='news-list']//h3//a[1]"):
            href = news_link.xpath("@href").extract_first()
            yield scrapy.Request(url="https://jheegusah.com/"+href,callback=self.get_news)

    def get_news(self, response):
        headline =response.xpath("//div[@class='news-section-title']//h2//text()").extract_first()
        date =response.xpath("(//p/text()[3])[1]").extract_first()
        final_news =[]
        for news in response.xpath("//span[@style='font-size: x-large;']//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news) ==0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))
            for news in response.xpath("//span[@style='color: #222222; font-family: Arial, Helvetica, "
                                      "sans-serif; font-size: x-large;']//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))
            for news in response.xpath("//div[@style='color: #222222; font-family: Arial, Helvetica, sans-serif; "
                                       "font-size: small;'][position()>1]//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))


        self.writer.writerow([headline, " ".join(final_news), date])
        yield {'headline': headline, 'final_news': " ".join(final_news),
               "date": date}
        # yield None



class JheegushaForeignNewsScraperSpider(scrapy.Spider):
    name = "jheegu_foreign_news"
    custom_settings = dict(LOG_ENABLED=False)
    start_urls = [
        f"https://jheegusah.com/news/%E0%A4%85%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%" \
        f"A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page={i}" for i in range(0, 53)]

    def __init__(self):
        self.outfile = open("../csv/jheegu_news_foreign.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news',"date"])

    def close(self, reason):
        self.outfile.close()

    def parse(self, response, **kwargs):
        for news_link in response.xpath("//ul[@class='news-list']//h3//a[1]"):
            href = news_link.xpath("@href").extract_first()
            yield scrapy.Request(url="https://jheegusah.com/"+href,callback=self.get_news)

    def get_news(self, response):
        headline =response.xpath("//div[@class='news-section-title']//h2//text()").extract_first()
        date =response.xpath("(//p/text()[3])[1]").extract_first()
        final_news =[]
        for news in response.xpath("//span[@style='font-size: x-large;']//text()").extract():
            final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news) ==0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))
            for news in response.xpath("//span[@style='color: #222222; font-family: Arial, Helvetica, "
                                      "sans-serif; font-size: x-large;']//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))
            for news in response.xpath("//div[@style='color: #222222; font-family: Arial, Helvetica, sans-serif; "
                                       "font-size: small;'][position()>1]//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))


        self.writer.writerow([headline, " ".join(final_news), date])
        yield {'headline': headline, 'final_news': " ".join(final_news),
               "date": date}
        # yield None


