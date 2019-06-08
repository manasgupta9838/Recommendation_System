import scrapy


class LinkSpider(scrapy.Spider):
    name = 'linkscraper'
    baseurl = 'https://www.amazon.in'

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 3,

    }

    def __init__(self, search='mobiles', name="linkscraper", **kwargs):
        self.start_urls = [f"https://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={search}"]
        super().__init__(name, **kwargs)

    def parse(self, response):
        baseurl = self.baseurl
        links = response.css("a::attr(href)")
        for pos, link in enumerate(links):
            url = link.extract()
            if baseurl not in url and "http://www.amazon.in" not in url:
             url = baseurl + url
            yield {
                    'sno': pos,
                    'link': url,
                }


        # for next_page in response.css('div.prev-post > a'):
        #     yield response.follow(next_page, self.parse)
