import scrapy
from scrapy.crawler import CrawlerProcess
import pymongo


def connect_mongo():
    url = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(url)
    db = client['aggieChallenge']
    collection = db['articles']
    return collection


class ArticleSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://weather.com/',
        'https://www.wunderground.com/',
        'http://www.weather.gov/',
        'http://weather.weatherbug.com/',
        'http://www.cnn.com/'
        'http://www.foxnews.com/',
        'https://www.huffingtonpost.com/',
        'http://abcnews.go.com/',
        'https://www.wsj.com/',
        'https://www.forbes.com/',
        'https://www.nytimes.com/',
        'https://www.cbsnews.com/',
        'https://www.yahoo.com/news/',
        'https://www.usatoday.com/',
        'https://www.nbcnews.com/',
        'https://www.washingtonpost.com/',
        'http://www.latimes.com/',
        'https://news.google.com/news/',
        'http://www.chicagotribune.com/',
        'http://www.chron.com/',
        'http://nypost.com/',
        'http://www.sfgate.com/',
        'http://www.npr.org/',
        'http://cbslocal.com/',
        'http://www.bbc.com/',
        'http://www.espn.com/'
    ]

    def parse(self, response):
        # in json return title and link TODO get publication date

        # SENDS TO FEED URI FILE
        # yield {
        #     'title': response.css('title').extract_first(),
        #     'link': response.url
        # }

        # SENDS TO MONGODB SERVER
        mongo_collection.insert_one({
            'title': response.css('title').extract_first(),
            'link': response.url
        })

        # get links to crawl
        for a in response.css('a'):
            yield response.follow(a, callback=self.parse)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'JOBDIR': 'crawls/article_spider'
    # 'FEED_FORMAT': 'jsonlines',
    # 'FEED_URI': 'pages.json'
})

global mongo_collection
mongo_collection = connect_mongo()
process.crawl(ArticleSpider)
process.start() # the script will block here until the crawling is finished