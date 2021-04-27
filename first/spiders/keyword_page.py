import scrapy
from bs4 import BeautifulSoup
from ..items import Keyword_page
import numpy as np


mystring = '/keywords?ref_=tt_stry_kw'


class KeyWordsSpider (scrapy.Spider):
    name = 'key_words'
    with open(r"usa_gross_urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    start_urls = [s + mystring for s in start_urls]
    # start_urls = start_urls[-2:]


    # start_urls = ['https://www.imdb.com/title/tt4154796/keywords?ref_=tt_stry_kw']


    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        items = Keyword_page()
        full_url_list = response.request.url.split("/")
        items['movie_id'] = full_url_list[4]

        key_words = []
        key_relevance = []
        odds = response.css('tr.odd')
        evens = response.css('tr.even')
        if len(odds) != 0:
            for odd in odds:
                sodas = odd.css('td')
                for soda in sodas:
                    keyword_cont = soda.css('div.sodatext')
                    keyword = keyword_cont.css('a::text').extract_first()
                    relevance_cont = soda.css('div.interesting-count-text')
                    relevance_text = relevance_cont.css('a::text').extract_first()
                    if (relevance_text == None):
                        continue
                    numbers = [int(s) for s in relevance_text.split() if s.isdigit()]
                    if ('?' in relevance_text):
                        continue
                    elif (numbers[1] == 1):
                        continue
                    a = numbers[0] / numbers[1]
                    key_words.append(keyword)
                    key_relevance.append("%.2f" % a)
            for even in evens:
                sodas = even.css('td')
                for soda in sodas:
                    keyword_cont = soda.css('div.sodatext')
                    keyword = keyword_cont.css('a::text').extract_first()
                    relevance_cont = soda.css('div.interesting-count-text')
                    relevance_text = relevance_cont.css('a::text').extract_first()
                    if (relevance_text == None):
                        continue
                    numbers = [int(s) for s in relevance_text.split() if s.isdigit()]
                    if ('?' in relevance_text):
                        continue
                    elif (numbers[1] == 1):
                        continue
                    a = numbers[0] / numbers[1]
                    key_words.append(keyword)
                    key_relevance.append("%.2f" % a)

        items['keywords'] = key_words
        items['keywords_relevance'] = key_relevance

        yield items





