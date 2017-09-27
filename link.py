from lxml import html
import requests
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class Link:
    def __init__(self, url, trusted=False):
        print(url)
        #TODO catch error for length
        self.protocol = url[0]
        self.site = url[2] # we ignore url[1] since it will always be blank
        if len(url) > 3:
            self.extension = "/".join(url[3:-1])
        else:
            self.extension = "/"

        self.link = "/".join(url)
        self.tree = None
        self.visited = False
        self.trusted = trusted
        self.children = []

    def goto(self):
        if not self.visited:
            destination = self.build_url()
            page = requests.get(destination)
            self.tree = html.fromstring(page.content)
            self.visited = True

    def crawl(self, trusted_sites=[]):
        for url in self.tree.xpath('//a/@href'):
            if len(url) > 0:
                valid = self.validate_url(url)
                if not valid and url[0] == '/' :
                    # if starts with '//' remove them and try again
                    if len(url) > 1 and url[1] == '/':
                        url = url[2:-1]
                        valid = self.validate_url(url)
                    else:
                        # build the url and add if it's an extension
                        self.children.append(Link(self.build_url(url).split("/"), True))
                # test if our link is 'long enough'
                if valid:
                    link = Link(url.split("/"))
                    # if this is an outside link test it's trust worthiness
                    link = Link(url, (link.site in trusted_sites))
                    self.children.append(link)

        return self.children

    def build_url(self, extension=None):
        if extension is None:
            extension = self.extension

        url = '{0}//{1}/{2}'.format(self.protocol, self.site, extension)
        return url

    def validate_url(self, url):
        val = URLValidator()
        try:
            val(url)
        except ValidationError as e:
            pass
        else:
            return True

        return False