import scrapy
from bs4 import BeautifulSoup
from ..items import Mini_page
import numpy as np


# url_file = open("usa_gross_urls.txt", "a")

class NewFilmSpider (scrapy.Spider):
    name = 'films_extra'
    with open(r"2020_urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    # start_urls = ['https://www.imdb.com/title/tt4154796/']

    # start_urls = start_urls[-5:]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        items = Mini_page()
        article = response.xpath('//div[@id="titleDetails"]')
        full_url_list = response.request.url.split("/")
        items['movie_id'] = full_url_list[4]
        items['links'] = []
        items['country'] = np.NaN
        items['language'] = np.NaN
        for block in article.css('div.txt-block'):
            block_content = block.extract()
            if "Official Sites" in block_content:
                site_links = []
                for site_link in block.css('a::text'):
                    txt = site_link.extract()
                    if not (txt in ['See more', 'Official Facebook',
                                    'Official Facebook Page']):
                        site_links.append(site_link.extract())
                items['links'] = site_links
            if "Country" in block_content:
                countries = []
                for country_link in block.css('a::text'):
                    txt = country_link.extract()
                    if not (txt in ['See more']):
                        countries.append(country_link.extract())
                items['country'] = countries
            if "Language" in block_content:
                languages = []
                for lang_link in block.css('a::text'):
                    txt = lang_link.extract()
                    if not (txt in ['See more']):
                        languages.append(lang_link.extract())
                items['language'] = languages

        yield items





