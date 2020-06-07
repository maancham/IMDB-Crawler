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
            genres_container = response.css('div.subtext')
            genres = genres_container.css('a::text').extract()
            director_writer = response.css('div.credit_summary_item')
            director = director_writer.css('a::text')[0].extract()
            writer = director_writer.css('a::text')[1].extract()
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
            items['date'] = date[:-1]
            items['genres'] = genres[:-1]
            items['director'] = director
            items['writer'] = writer
            items['cast'] = casts
            items['budget'] = money[43:]
            items['gross'] = gross[48:]

            if ((items['budget'] == "")):
                yield None

            rating_detail_ext = 'ratings'
            review_cont = response.xpath('//div[@id="titleUserReviewsTeaser"]')
            comment_tag = review_cont.xpath("//div[@class='user-comments']")
            rating_page = response.url + rating_detail_ext
            if (len(comment_tag) != 0):            
                review_page = response.css('div.user-comments a::attr(href)')[-1].get()
            else:
                review_page = None
            
            if not(rating_page is None):
                rating_file.write(rating_page + '\n')


            # if not(rating_page is None):
            #     yield response.follow(rating_page, callback=self.parserate)

            # if review_page is not None:
            #     yield response.follow(review_page, callback=self.parserev)


            yield items


            next_pages = response.css('div.rec_item a::attr(href)').getall()
            if next_pages is not None:
                for page in next_pages:
                    yield response.follow(page, callback= self.parse)
        else:
            yield None
               
        

class RateSpider (scrapy.Spider):
    name = 'rates'
    main_domain = 'https://www.imdb.com'
    with open("ratings.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]
    def parserate(self, response):

        items = Rating_page() 
        header = response.css('h3')[0]
        movie_name = header.css('a::text').extract()
        chart_ratings = [[0 for x in range(3)] for y in range(10)]
        detailed_ratings = [[0 for x in range(6)] for y in range(4)]
        top_us_nonus = [[0 for x in range(3)] for y in range(2)]

        j = 0
        for i in range(9,0,-1):
            chart_ratings[j][0] = i+1
            j+= 1
        chart_ratings[9][0] = 1

        detailed_ratings[0][0] = '-'
        detailed_ratings[0][1] = 'All ages'
        detailed_ratings[0][2] = '<18'
        detailed_ratings[0][3] = '18-29'
        detailed_ratings[0][4] = '30-44'
        detailed_ratings[0][5] = '45+'
        detailed_ratings[1][0] = 'All:'
        detailed_ratings[2][0] = 'Males:'
        detailed_ratings[3][0] = 'Females:'

        top_us_nonus[0][0] = 'Top 1000 Voters'
        top_us_nonus[0][1] = 'US users'
        top_us_nonus[0][2] = 'Non-US users'

        soup = BeautifulSoup(response.body, 'html5lib')
        containers = soup.findAll('table')

        charts = containers[0]
        weights = charts.findAll(
            'div', attrs={'class': 'topAligned'})
        volumes = charts.findAll(
            'div', attrs={'class': 'leftAligned'})
        volumes = volumes[1:]
        j = 0
        for i in range(len(weights)):
            chart_ratings[j][1] = weights[i].text.strip()
            chart_ratings[j][2] = volumes[i].text
            j+= 1
        
        demographic = containers[1]
        noexist_points_indexes = []
        all_dems_big_cell = demographic.findAll(
            'div', attrs={'class': 'bigcell'})
        for i in range(len(all_dems_big_cell)):
            if (all_dems_big_cell[i].text == '-'):
                noexist_points_indexes.append(i)
        all_dems_small_cell = demographic.findAll(
            'div', attrs={'class': 'smallcell'})
        for i in range(len(noexist_points_indexes)):
            all_dems_small_cell.insert(noexist_points_indexes[i], '-')
        row_number = 1
        for i in range(len(all_dems_big_cell)):
            
            point = all_dems_big_cell[i].text
            if(all_dems_small_cell[i] == '-'):
                point_volume = '-'
            else:
                point_volume = all_dems_small_cell[i].text.strip()
            if (row_number == 4):
                break
            j = ((i+1)%6 + row_number-1) % 6
            detailed_ratings[row_number][j] = point + '/' + point_volume
            if (i == 4) or (i == 9):
                row_number += 1

        extra_details = containers[2]
        extra_big_cell = extra_details.findAll(
            'div', attrs={'class': 'bigcell'})
        extra_small_cell = extra_details.findAll(
            'div', attrs={'class': 'smallcell'})
        for i in range(len(extra_big_cell)):
            point = extra_big_cell[i].text
            point_volume = extra_small_cell[i].text.strip()
            top_us_nonus[1][i] = point + '/' + point_volume

        items['name'] = movie_name[0]
        items['chart'] = chart_ratings
        items['detail'] = detailed_ratings
        items['extra'] = top_us_nonus

        yield items


    def parserev(self, response):

        header = response.css('h3')[0]
        movie_name = header.css('a::text').extract()

        def convert_to_int(st):
            if(len(st) <= 3):
                return(int(st))
            else:
                ind = st.find(',')
                new_st = st[0:ind] + st[ind+1:]
                return(int(new_st))

        driver = webdriver.Firefox()
        driver.get(response.url)
        while True:
            try:
                loadmore = driver.find_element_by_id("load-more-trigger")
                time.sleep(1)
                loadmore.click()
                time.sleep(0.5)
            except Exception as e:
                break

        NoneType = type(None)
        ratings = []
        user_names = []
        dates = []
        helpful_info = []

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        items = Review_page()

        review_container = soup.findAll(
            'div', attrs={'class': 'lister-item-content'})
        for review in review_container:
            rating_container = review.find(
                'span', attrs={'class': 'rating-other-user-rating'})
            name_date_container = review.find(
                'div', attrs={'class': 'display-name-date'})
            helpful_container = review.find('div', attrs={'class': 'content'})
            for h in helpful_container.findAll('div', attrs={'class': 'text-muted'}):
                pretty_text = h.text.strip()
                first_line = pretty_text.partition('\n')[0].split()
                if(convert_to_int(first_line[3]) == 0):
                    helpful_info.append("-")
                    continue
                else:
                    helpful_info.append(
                        str(int(convert_to_int(first_line[0])/convert_to_int(first_line[3]) * 100)) + "%")
            for name in name_date_container.findAll('a'):
                raw_name = name.text
                cleaned_name = raw_name.replace('.', '_')
                user_names.append(cleaned_name)
            for date in name_date_container.findAll('span', attrs={'class': 'review-date'}):
                dates.append(date.text)
            if(type(rating_container) == NoneType):
                ratings.append("-")
                continue
            for r in rating_container.findAll('span'):
                if(int(r.text) >= 0 and int(r.text) <= 10):
                    ratings.append(int(r.text))
                    break

        driver.quit()

        revs = dict(zip(user_names, zip(ratings, helpful_info, dates)))
        items['data'] = revs
        items['name'] = movie_name[0]
        yield items
