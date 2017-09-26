from lxml import html
import requests
page = requests.get('http://www.cnn.com/')
tree = html.fromstring(page.content)

urls = tree.xpath('//a/@href')

print(urls)