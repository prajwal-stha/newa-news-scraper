import scrapy


class NewaWikipediaScraper(scrapy.Spider):

    name = "newa_wiki"


    start_urls = ["https://new.wikipedia.org/wiki/%E0%A4%AE%E0%A5%82_%E0%A4%AA%E0%A5%8C"]

    def parse(self, response, **kwargs):

        # for name in response.xpath("//*[@id='mw-content-text']/div[1]/table[3]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody//td//b//a//big/text()"):
        #     pass
        # print(name.extract())

        for data in response.xpath(
                "//*[@id='mw-content-text']/div[1]/table[3]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody//td[not(@align='center')]//span[not(@class='plainlinks')]//p//a/@href").extract():
            yield scrapy.Request(url=response.urljoin(data), callback=self.get_info)

    def get_info(self, response):
        if response.xpath("//div[@class='mw-parser-output']//ol//li"):
            for urls in response.xpath("//div[@class='mw-parser-output']//ol//li//a/@href").extract():
                yield scrapy.Request(url=response.urljoin(urls), callback=self.get_inner_info)
        else:
            print("hi" * 100)

    def get_inner_info(self, response):
        print(response.url)
