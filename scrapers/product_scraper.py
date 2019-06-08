import scrapy
import numpy as np
import pandas as pd


def get_product_urls(path):
    df = pd.read_csv(path)
    has_dp = df.link.str.contains('/dp')
    has_http = df.link.str.contains('http')
    productdf = df[has_http & has_dp]
    print(productdf)
    return list(set(productdf.link.tolist()))


class ProductSpider(scrapy.Spider):
    name = 'productscraper'
    # start_urls = get_product_urls("../data/link_oct3.csv")

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 3,

    }

    def __init__(self, path='../data/link_oct3.csv', name='productscraper', **kwargs):
        self.start_urls = get_product_urls(path)
        super().__init__(name, **kwargs)

    def parse(self, response):

        try:
            title = response.css("#productTitle::text").extract_first().replace('\n', '').strip()
        except Exception as e:
            print(e)
            title = np.nan
        company = response.css("#bylineInfo::text").extract_first()
        customerreviews = response.css(".arp-rating-out-of-text::text").extract_first()
        try:
            rating = response.css("#acrPopover::attr(title)").extract_first().split()[0]
            rating = float(rating)
        except Exception as e:
            rating = np.nan
        try:
            reviews = response.css("#acrCustomerReviewText::text").extract_first().split()[0]
            reviews = reviews.replace(',', '')
            reviews = int(reviews)
        except Exception as e:
            reviews = np.nan
        try:
            price = response.css('#priceblock_ourprice::text').extract_first()
            if len(price):
                try:
                    price = price.replace('₹', '')
                    price = price.replace(u'\xa0', '')
                except:
                    pass
                try:
                    price = price.replace(',', '')
                    price = price.split()[0]
                except:
                    pass
                try:
                    price = float(price)
                except:
                    price = price
            else:
                price = price
        except Exception as e:
            price = response.css('#priceblock_dealprice::text').extract_first()
        except:
            price = np.nan

        yield {
            'title': title,
            'price': price,
            'reviews': reviews,
            'rating': rating,
            'company': company,
            'customerreviews': customerreviews,
            'link': response.url
        }
