import scrapy
from bs4 import BeautifulSoup
from ..items import Cast_page
import numpy as np


# url_file = open("usa_gross_urls.txt", "a")
mystring = 'fullcredits?ref_=tt_cl_sm#cast'


class CastFilmSpider (scrapy.Spider):
    name = 'casts'
    with open(r"2020_urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    start_urls = [s + mystring for s in start_urls]


    # start_urls = ['https://www.imdb.com/title/tt4154796/fullcredits?ref_=tt_cl_sm#cast']


    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        items = Cast_page()
        full_url_list = response.request.url.split("/")
        items['movie_id'] = full_url_list[4]

        casts = []
        casts_id = []
        casts_container = response.css('table.cast_list')
        odd_casts = casts_container.css('tr.odd')
        even_casts = casts_container.css('tr.even')
        if len(casts_container) != 0:
            for cast in odd_casts:
                actor_name_cont = cast.css('td')[1]
                actor_name = actor_name_cont.css('a::text').extract()
                actor_id = actor_name_cont.css('a::attr(href)').extract_first()
                string_name = ''.join(actor_name)
                casts.append(string_name.strip())
                casts_id.append(actor_id)
            for cast in even_casts:
                actor_name_cont = cast.css('td')[1]
                actor_name = actor_name_cont.css('a::text').extract()
                actor_id = actor_name_cont.css('a::attr(href)').extract_first()
                string_name = ''.join(actor_name)
                casts.append(string_name.strip())
                casts_id.append(actor_id)

        items['casts'] = casts
        items['casts_id'] = casts_id

        yield items





