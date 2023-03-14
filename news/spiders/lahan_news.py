import scrapy, csv
from urllib.parse import urljoin


class LahanNationalNewsScraperSpider(scrapy.Spider):
    itemlist = []
    custom_settings = dict(LOG_ENABLED=False)
    name = "lahan_ntional_news"
    start_urls = [
        f"https://www.lahananews.com/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%B0%E0%A4%BE%E0%A4%B7%E0%A5%8D%E0%A4"
        f"%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page={i}" for i in range(0, 524)
    ]

    def __init__(self):
        self.outfile = open("news/csv/lahan_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news', 'date'])

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

        if len(final_news) == 0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news) > 0:
            self.writer.writerow([" ".join(headline), " ".join(final_news), " ".join(date)])
            yield {'headline': " ".join(headline), 'final_news': " ".join(final_news), "date": " ".join(date)}


class LahanForeignNewsScraperSpider(scrapy.Spider):
    itemlist = []
    custom_settings = dict(LOG_ENABLED=False)
    name = "lahan_foreign_news"
    start_urls = [
        f"https://www.lahananews.com/%E0%A4%AC%E0%A5%81%E0%A4%96%E0%A4%81/%E0%A4%85%E0%A4%A8%E0%A5%8D%E0%A4%A4%E0%A4%B0%E0%A5%8D%E0%A4%B0%E0%A4%" \
        f"BE%E0%A4%B7%E0%A5%8D%E0%A4%9F%E0%A5%8D%E0%A4%B0%E0%A4%BF%E0%A4%AF?page=0{i}" for i in range(0, 83)
    ]

    def __init__(self):
        self.outfile = open("../csv/lahan_foreign_news.csv", "w", newline="", encoding="utf-8-sig")
        self.writer = csv.writer(self.outfile)
        self.writer.writerow(['headline', 'final_news', 'date'])

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

        if len(final_news) == 0:
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " "))

        if len(final_news) > 0:
            self.writer.writerow([" ".join(headline), " ".join(final_news), " ".join(date)])
            yield {'headline': " ".join(headline), 'final_news': " ".join(final_news), "date": " ".join(date)}


class LahanNewsScraperSpider(scrapy.Spider):
    """
    class to extarct news of lahan website
    """
    name = 'lahan_news'
    custom_settings = {'LOG_ENABLED': False, 'ITEM_PIPELINES': {'news.pipelines.LahanNewsCategoryCsvPipeline': 401}}
    # custom_settings = {'LOG_ENABLED': False}
    start_urls = ["https://www.lahananews.com/"]

    def parse(self, response, **kwargs):
        """
        first visit and find the links of all categories and pass url to next method
        :param response:
        :param kwargs:
        :return:
        """
        for link in response.xpath("//li[@class='expanded leaf']//ul//li//a"):
            href = link.attrib['href']
            url = urljoin(response.url, href)
            yield scrapy.Request(url=url, callback=self.get_news_category)

    def get_news_category(self, response):
        """
        find the specific new category and also the page size upto
        which the website needs to loop over
        :param response: dict
        :return: None
        """
        url = response.xpath("//div[@class='item-list']//ul//li[@class='pager-last last']//a")
        href = url.attrib['href']
        page_sizes = int(href.split('=')[1])
        for news in range(0, page_sizes):
            yield scrapy.Request(url=response.url + f"?page={news}",
                                 callback=self.get_news_tabs,
                                 )

    def get_news_tabs(self, response):
        """
        Now go to  news tab link i.e National news page 1 upto last page and pass
        the detail url to get news
        :param response:
        :return:
        """
        category = response.xpath("//div[@class='news-section-title']//h2/text()").get().strip()
        for news_link in response.xpath("//div[@class='hot-news-box']//li//div//h3//a/@href").extract():
            yield scrapy.Request(url="https://www.lahananews.com/" + news_link,
                                 callback=self.get_news, meta={'news_category': category})

    def get_news(self, response):
        """
        finally catch all the news
        :param response: dict
        :return:
        """
        headline = (response.xpath("//div[@class='news-section-title']//h2//text()").extract())
        date = response.xpath("//div[@class='content']/p//text()").extract()
        new_date = list(map(lambda x: x.strip(), filter(lambda x: x.strip() != "", date)))

        category = response.meta.get('news_category')

        final_news = []
        if response.xpath("//span[@style='font-size:18px;']//text()"):
            for news in response.xpath("//span[@style='font-size:18px;']//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " ").replace("\n", ""))

            yield ({'headline': " ".join(headline),
                    'final_news': " ".join(final_news),
                    "date": " ".join(new_date),
                    "category": category,
                    "url": response.url
                    })

        if response.xpath("//div[@class='cms-content']//p//text()"):
            for news in response.xpath("//div[@class='cms-content']//p//text()").extract():
                final_news.append(news.replace(' ', ' ').replace(" ", " ").replace("\n", ""))
            yield {'headline': " ".join(headline),
                   'final_news': " ".join(final_news),
                   "date": " ".join(new_date),
                   "category": category,
                   "url": response.url
                   }
