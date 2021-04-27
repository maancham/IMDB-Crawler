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
    if (len(not_ready) != 0) or (series_code in date) or (video_code in date):
        return False
    return True

      

class FilmSpider (scrapy.Spider):
    name = 'films'
    with open(r"2020_urls.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    # start_urls = start_urls[0:]

    # start_urls = ['https://www.imdb.com/title/tt00000848228/']
    def parse(self, response):
        rating_file = open("ratings.txt", "a")
        review_file = open("reviews.txt", "a")
        is_serie = False
        items = Main_page()
        not_ready = response.xpath("//div[@class='status-message-heading']")

        items['date'] = np.NaN
        date_container = response.css('div.subtext')
        date = date_container.css('a::text')
        if len(date) != 0:
            date = date[-1].extract()
            items['date'] = date[:-1]

        if first_field_check(not_ready, date):
            full_url_list = response.request.url.split("/")
            items['movie_id'] = full_url_list[4]
            header = response.css('h1::text').extract_first()
            org_title_container = response.css('div.originalTitle::text')
            if len(org_title_container) == 1:
                items['org_name'] = org_title_container.extract_first()
            else:
                items['org_name'] = np.NaN

            title_year_container = response.css('span#titleYear')
            title_year = title_year_container.css('a::text').extract_first()

            items['point'] = np.NaN
            items['point_volume'] = np.NaN
            rating_container = response.css('div.ratingValue')
            if len(rating_container) != 0:
                rating = rating_container.css('span::text')[0].extract()
                rating_volume = response.css('span.small::text').extract_first()
                items['point'] = float(rating)
                items['point_volume'] = rating_volume


            full_genres_container = response.xpath("//div[@class='see-more inline canwrap']")
            if len(full_genres_container) == 2:
                full_genres_list = full_genres_container[1].css('a::text').extract()
            else:
                full_genres_list = full_genres_container.css('a::text').extract()
            full_genres_list = [s[1:] for s in full_genres_list]


            items['director'] = np.NaN
            items['writer'] = np.NaN
            director_writer = response.css('div.credit_summary_item')
            directors = []
            writers = []
            if not(director_writer is None):
                for block in director_writer:
                    block_content = block.extract()
                    if "Directors" in block_content:
                        for director_link in director_writer[0].css('a::text'):
                            directors.append(director_link.extract())
                        items['director'] = directors
                    elif "Writers" in block_content:
                        for writer_link in director_writer[1].css('a::text'):
                            writers.append(writer_link.extract())
                        items['writer'] = writers


            items['user_reviews'] = np.NaN
            items['critic_reviews'] = np.NaN
            reviews_count_container = response.xpath("//div[@class='titleReviewBarItem titleReviewbarItemBorder']")
            if len(reviews_count_container) != 0:
                reviews_count_div = reviews_count_container.css('span.subText')
                for revs_count in reviews_count_div.css('a::text'):
                    if "user" in revs_count.extract():
                        items['user_reviews'] = revs_count.extract()
                    elif "critic" in revs_count.extract():
                        items['critic_reviews'] = revs_count.extract()


            metascore = response.xpath(
                "//div[@class='metacriticScore score_favorable titleReviewBarSubItem']//text()").extract()
            if len(metascore) == 0:
                items['metascore'] = np.NaN
            else:
                items['metascore'] = int(metascore[1])


            items['story_line'] = np.NaN
            items['plt_keywords'] = np.NaN
            story_article = response.xpath('//div[@id="titleStoryLine"]')
            story_container = story_article.xpath("//div[@class='inline canwrap']")
            plt_keyword_container = story_article.xpath("//div[@class='see-more inline canwrap']")
            if len(story_container) != 0:
                items['story_line'] = story_container.css('span::text').extract_first().lstrip()
            if len(plt_keyword_container) != 0:
                for container in plt_keyword_container:
                    if "Plot" in container.css('h4::text').extract_first():
                        keywords = []
                        for key_link in container.css('span.itemprop::text'):
                            if not("See more" in key_link.extract()):
                                keywords.append(key_link.extract())
                        items['plt_keywords'] = keywords



            article = response.xpath('//div[@id="titleDetails"]')
            items['country'] = np.NaN
            items['language'] = np.NaN
            items['budget'] = np.NaN
            items['world_gross'] = np.NaN
            items['usa_gross'] = np.NaN
            items['runtime'] = np.NaN
            for block in article.css('div.txt-block'):
                block_content = block.extract()
                if "Country" in block_content:
                    countries = []
                    for country_link in block.css('a::text'):
                        countries.append(country_link.extract())
                    items['country'] = countries
                if "Language" in block_content:
                    languages = []
                    for lang_link in block.css('a::text'):
                        languages.append(lang_link.extract())
                    items['language'] = languages
                if "Budget" in block_content:
                    money = block_content.splitlines()[1]
                    items['budget'] = money[43:]
                elif "Worldwide" in block_content:
                    world_gross = block_content.splitlines()[1]
                    world_gross = world_gross.replace('</div>', '').replace(' ', '')
                    items['world_gross'] = world_gross[48:]
                elif "Gross USA" in block_content:
                    usa_gross = block_content.splitlines()[1]
                    usa_gross = usa_gross.replace('</div>', '').replace(' ', '')
                    items['usa_gross'] = usa_gross[32:]
                elif "Production" in block_content:
                    pro_companies = []
                    for comp_link in block.css('a::text'):
                        if not("See more" in comp_link.extract()):
                            pro_companies.append(comp_link.extract().lstrip())
                    items['production_companies'] = pro_companies
                elif "Runtime" in block_content:
                    runtime_container = block.css('time::text').extract_first()
                    runtime = [int(s) for s in runtime_container.split() if s.isdigit()]
                    items['runtime'] = runtime[0]


            casts = []
            casts_container = response.css('table.cast_list')
            odd_casts = casts_container.css('tr.odd')
            even_casts = casts_container.css('tr.even')
            if (not is_serie) and (len(casts_container) != 0):
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
            items['title_year'] = int(title_year)
            items['genres'] = full_genres_list
            items['cast'] = casts


            rating_detail_ext = 'ratings'
            review_cont = response.xpath('//div[@id="titleUserReviewsTeaser"]')
            comment_tag = review_cont.xpath("//div[@class='user-comments']")
            rating_page = response.url + rating_detail_ext
            if len(comment_tag) != 0:
                review_page = response.css('div.user-comments a::attr(href)')[-1].get()
            else:
                review_page = None

            if not(rating_page is None):
                rating_file.write(rating_page + '\n')
            if not(review_page is None):
                review_file.write("https://www.imdb.com" + review_page + '\n')

            yield items



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
