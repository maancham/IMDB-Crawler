import scrapy
from selenium import webdriver
from bs4 import BeautifulSoup
from ..items import Main_page, Rating_page, Review_page
from scrapy.http import HtmlResponse
import re
import numpy as np
import time
import requests
import os
import sys

error_list = []
series_code = "TV"
video_code = "Video"

def first_field_check(not_ready, date):
    if ((len(not_ready) != 0) or (series_code in date) or (video_code in date)):
        return False
    return True


class FilmSpider (scrapy.Spider):
    name = 'films'
    main_domain = 'https://www.imdb.com'
    start_urls = [
        'https://www.imdb.com/title/tt0451279'
    ]

    a = 'tt0451279'
    def parse(self, response):
        rating_file = open("ratings.txt", "a")
        is_serie = False
        items = Main_page()
        casts = []
        not_ready = response.xpath("//div[@class='status-message-heading']")
        date_container = response.css('div.subtext')
        date = date_container.css('a::text')[-1].extract()
        if (first_field_check(not_ready, date)):
            header = response.css('h1::text').extract_first()

            rating_container = response.css('div.ratingValue')
            rating = rating_container.css('span::text')[0].extract()
            rating_volume = response.css('span.small::text').extract_first()
            # genres_container = response.css('div.subtext')
            # genres = genres_container.css('a::text').extract()

            full_genres_container = response.xpath("//div[@class='see-more inline canwrap']")[1]
            full_genres_list = full_genres_container.css('a::text').extract()
            full_genres_list = [s[1:] for s in full_genres_list]

            director_writer = response.css('div.credit_summary_item')
            director = director_writer.css('a::text')[0].extract()
            writer = director_writer.css('a::text')[1].extract()

            metascore = response.xpath(
                "//div[@class='metacriticScore score_favorable titleReviewBarSubItem']//text()").extract()

            article = response.xpath('//div[@id="titleDetails"]')


            money = ""
            gross = ""
            for block in article.css('div.txt-block'):
                block_content = block.extract()
                if ("Budget" in block_content):
                    money = block_content.splitlines()[1]
                elif ("Worldwide" in block_content):
                    gross = block_content.splitlines()[1]
                    gross = gross.replace('</div>', '').replace(' ', '')
            
            casts_container = response.css('table.cast_list')
            odd_casts = casts_container.css('tr.odd')
            even_casts = casts_container.css('tr.even')
            if (not is_serie):
                for cast in odd_casts:
                    actor_name_cont = cast.css('td')[1]
                    actor_name = actor_name_cont.css('a::text').extract()
                    string_name = ''.join(actor_name)
                    casts.append(string_name.strip())
                for cast in even_casts:
                    actor_name_cont = cast.css('td')[1]
                    actor_name = actor_name_cont.css('a::text').extract()
                    string_name = ''.join(actor_name)
                    casts.append(string_name.strip())

            items['name'] = header[0:-1]
            items['point'] = rating
            items['point_volume'] = rating_volume
            items['metascore'] = int(metascore[1])
            items['date'] = date[:-1]
            items['genres'] = full_genres_list
            items['director'] = director
            items['writer'] = writer
            items['cast'] = casts
            items['budget'] = money[43:]
            items['gross'] = gross[48:]

            if ((items['budget'] == "")):
                yield None

            # rating_detail_ext = 'ratings'
            # review_cont = response.xpath('//div[@id="titleUserReviewsTeaser"]')
            # comment_tag = review_cont.xpath("//div[@class='user-comments']")
            # rating_page = response.url + rating_detail_ext
            # if (len(comment_tag) != 0):            
            #     review_page = response.css('div.user-comments a::attr(href)')[-1].get()
            # else:
            #     review_page = None
            
            # if not(rating_page is None):
            #     rating_file.write(rating_page + '\n')


            # if not(rating_page is None):
            #     yield response.follow(rating_page, callback=self.parserate)

            # if review_page is not None:
            #     yield response.follow(review_page, callback=self.parserev)


            yield items


            # next_pages = response.css('div.rec_item a::attr(href)').getall()
            # if next_pages is not None:
            #     for page in next_pages:
            #         yield response.follow(page, callback= self.parse)
        else:
            yield None
               
        




    # def parserev(self, response):

    #     header = response.css('h3')[0]
    #     movie_name = header.css('a::text').extract()

    #     def convert_to_int(st):
    #         if(len(st) <= 3):
    #             return(int(st))
    #         else:
    #             ind = st.find(',')
    #             new_st = st[0:ind] + st[ind+1:]
    #             return(int(new_st))

    #     driver = webdriver.Firefox()
    #     driver.get(response.url)
    #     while True:
    #         try:
    #             loadmore = driver.find_element_by_id("load-more-trigger")
    #             time.sleep(1)
    #             loadmore.click()
    #             time.sleep(0.5)
    #         except Exception as e:
    #             break

    #     NoneType = type(None)
    #     ratings = []
    #     user_names = []
    #     dates = []
    #     helpful_info = []

    #     soup = BeautifulSoup(driver.page_source, 'html5lib')
    #     items = Review_page()

    #     review_container = soup.findAll(
    #         'div', attrs={'class': 'lister-item-content'})
    #     for review in review_container:
    #         rating_container = review.find(
    #             'span', attrs={'class': 'rating-other-user-rating'})
    #         name_date_container = review.find(
    #             'div', attrs={'class': 'display-name-date'})
    #         helpful_container = review.find('div', attrs={'class': 'content'})
    #         for h in helpful_container.findAll('div', attrs={'class': 'text-muted'}):
    #             pretty_text = h.text.strip()
    #             first_line = pretty_text.partition('\n')[0].split()
    #             if(convert_to_int(first_line[3]) == 0):
    #                 helpful_info.append("-")
    #                 continue
    #             else:
    #                 helpful_info.append(
    #                     str(int(convert_to_int(first_line[0])/convert_to_int(first_line[3]) * 100)) + "%")
    #         for name in name_date_container.findAll('a'):
    #             raw_name = name.text
    #             cleaned_name = raw_name.replace('.', '_')
    #             user_names.append(cleaned_name)
    #         for date in name_date_container.findAll('span', attrs={'class': 'review-date'}):
    #             dates.append(date.text)
    #         if(type(rating_container) == NoneType):
    #             ratings.append("-")
    #             continue
    #         for r in rating_container.findAll('span'):
    #             if(int(r.text) >= 0 and int(r.text) <= 10):
    #                 ratings.append(int(r.text))
    #                 break

    #     driver.quit()

    #     revs = dict(zip(user_names, zip(ratings, helpful_info, dates)))
    #     items['data'] = revs
    #     items['name'] = movie_name[0]
    #     yield items
