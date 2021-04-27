import scrapy
from bs4 import BeautifulSoup
# from ..items import Mini_page
import numpy as np


url_file = open("2020_urls.txt", "a")

class SearchFilmSpider (scrapy.Spider):
    name = 'search'
    with open(r"search_page_urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    # start_urls = ['https://www.imdb.com/title/tt4154796/']

    # start_urls = start_urls[0:2]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        containers = soup.find_all("h3", {"class": "lister-item-header"})
        for container in containers:
            link = ''
            link_cont = container.find_all("a", href=True)
            for row in link_cont:
                link = row['href']
            new_link =  'https://www.imdb.com' + link
            url_file.write(new_link + '\n')




