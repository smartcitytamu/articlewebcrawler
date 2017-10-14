import scrapy
from scrapy.crawler import CrawlerProcess

class KeywordsArticleSpider(scrapy.Spider):
    name = "articles"
    keywords = [
        'Hurricane',
        'hurricane',
        'Disaster',
        'disaster',
        'Electricity',
        'electricity',
        'Flooding',
        'flooding',
        'Power',
        'power',
        'Relief',
        'relief'
    ]
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
        # determine if response has keywords TODO improve this portion - may be being thrown out of this part of application
        keyword_exists = False
        for word in KeywordsArticleSpider.keywords:
            if word in response.text:
                keyword_exists = True
                break

        # in json return title and link TODO get publication date
        if keyword_exists:
            yield {
                'title': response.css('title').extract_first(),
                'link': response.url
            }
        # get links to crawl
        for a in response.css('a'):
            yield response.follow(a, callback=self.parse)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'JOBDIR': 'crawls/article_spider'
})

process.crawl(KeywordsArticleSpider)
process.start() # the script will block here until the crawling is finished