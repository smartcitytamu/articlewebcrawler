from lxml import html
import requests
import link
import queue


class Crawler:
    def __init__(self, seeds):
        self.link_queue = queue.Queue()
        self.visited_links = []
        self.trusted_source = []
        self._run = True
        # seed our crawler
        for seed in seeds:
            self.link_queue.put(link.Link(seed.split("/"), True))

        #Limit For Testing
        self.it = 10000;

    def run(self):
        while self._run and not self.link_queue.empty():
                # get a link to look at
                page = self.link_queue.get()
                # if we have not visited the link goto and crawl it
                if page.link not in self.visited_links: #and page.trusted:
                    page.goto()
                    self.visited_links.append(page.link)

                    #TODO do more stuff with a link
                    print("HIT! : " + page.link)

                    #crawl the page and add all it's links to our
                    for link in page.crawl():
                        self.link_queue.put(link)

                    self.it -= 1

                #Limit For Testing
                if self.it <= 0:
                    self._run = False

# a few seeds for testing
my_seeds = ['https://stn.wim.usgs.gov/FEV/#HarveyAug2017',
         'https://www.nvoad.org/hurricane-harvey/volunteer/',
         'https://oceanservice.noaa.gov/news/high-tide-bulletin/summer-2017/',
         'http://www.usace.army.mil/Media/News-Archive/Story-Article-View/Article/1298959/corps-of-engineers-researchers-use-supercomputer-to-model-harvey-flooding/',
         'https://www.washingtonpost.com/national/cajun-navy-races-from-louisiana-to-texas-using-boats-to-pay-it-forward/2017/08/28/1a010c8a-8c1f-11e7-84c0-02cc069f2c37_story.html']


my_crawler = Crawler(my_seeds)
my_crawler.run()


