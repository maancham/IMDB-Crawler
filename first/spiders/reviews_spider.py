# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import Review_page
import numpy as np


mystring = 'reviews'
imdb_tag = 'https://www.imdb.com'

class ReviewsSpider(scrapy.Spider):
    # name = 'review_links'
    #
    # with open(r"usa_movie_urls.txt", "rt") as f:
    #     start_urls = [url.strip() for url in f.readlines()]
    #
    # start_urls = start_urls[15966:]
    # start_urls = [s + mystring for s in start_urls]
    #
    # def parse(self, response):
    #     review_file = open("review_links.txt", "a")
    #     soup = BeautifulSoup(response.body, 'html5lib')
    #     full_url_list = response.request.url.split("/")
    #     containers = soup.find_all("div", {"class": "actions text-muted"})
    #     if (len(containers) != 0):
    #         for container in containers:
    #             link_containers = container.find_all("a", href=True)
    #             if (len(link_containers) == 2):
    #                 permalink_container = link_containers[1]
    #                 review_link = permalink_container['href']
    #                 review_link = imdb_tag + review_link
    #                 review_file.write(review_link + '\n')

    name = 'reviews'

    with open(r"review_links.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    # start_urls = [
    #     'https://www.imdb.com/review/rw6088797/',
    #     'https://www.imdb.com/review/rw3446333/'
    # ]

    start_urls = start_urls[589931:]

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        items = Review_page()
        parent_container = response.css('div.subpage_title_block')

        username_container = parent_container.css('div.parent')
        user_id = username_container.css('a::attr(href)').extract_first().split('/')[2]
        items['user_id'] = user_id

        movieId_container = parent_container.css('h1.header')
        movie_id =  movieId_container.css('a::attr(href)').extract_first().split('/')[2]
        items['movie_id'] = movie_id

        review_container = response.css('div.review-container')
        items['rating'] = np.NaN
        rating_container = review_container.css('span.rating-other-user-rating')
        if (len(rating_container) != 0):
            rating = int(rating_container.css('span::text').extract()[2])
            items['rating'] = rating

        items['title'] = review_container.css('a.title::text').extract_first().strip()

        items['date'] = review_container.css('span.review-date::text').extract_first().strip()

        text_container = soup.find("div", {"class": "text show-more__control"}).text
        text_container = review_container.xpath('//div[@class="text show-more__control"]/text()').get()
        items['text'] = text_container

        yield items


        # header = response.css('h3')[0]
        # movie_name = header.css('a::text').extract()
        #
        # def convert_to_int(st):
        #     if(len(st) <= 3):
        #         return(int(st))
        #     else:
        #         ind = st.find(',')
        #         new_st = st[0:ind] + st[ind+1:]
        #         return(int(new_st))

        # driver = webdriver.Firefox()
        # driver.get(response.url)
        # while True:
        #     try:
        #         loadmore = driver.find_element_by_id("load-more-trigger")
        #         time.sleep(1)
        #         loadmore.click()
        #         time.sleep(0.5)
        #     except Exception as e:
        #         break

        NoneType = type(None)
        ratings = []
        user_names = []
        dates = []
        helpful_info = []

        # soup = BeautifulSoup(driver.page_source, 'html5lib')
        # items = Review_page()

        # review_containers = response.css('div.review-container')
        # for container in review_containers:
        #     title_text = container.css('a.title::text').extract_first()
        #     if (len(title_text) != 0):
        #         items['titles'] = title_text.lstrip().rstrip()
        #     else:
        #         items['titles'] = np.NaN

        # review_container = soup.findAll('div', attrs={'class': 'lister-list'})
        # for review in review_container:
        #     rating_container = review.find(
        #         'span', attrs={'class': 'rating-other-user-rating'})
        #     name_date_container = review.find(
        #         'div', attrs={'class': 'display-name-date'})
        #     helpful_container = review.find('div', attrs={'class': 'content'})
        #     for h in helpful_container.findAll('div', attrs={'class': 'text-muted'}):
        #         pretty_text = h.text.strip()
        #         first_line = pretty_text.partition('\n')[0].split()
        #         if(convert_to_int(first_line[3]) == 0):
        #             helpful_info.append("-")
        #             continue
        #         else:
        #             helpful_info.append(
        #                 str(int(convert_to_int(first_line[0])/convert_to_int(first_line[3]) * 100)) + "%")
        #     for name in name_date_container.findAll('a'):
        #         raw_name = name.text
        #         cleaned_name = raw_name.replace('.', '_')
        #         user_names.append(cleaned_name)
        #     for date in name_date_container.findAll('span', attrs={'class': 'review-date'}):
        #         dates.append(date.text)
        #     if(type(rating_container) == NoneType):
        #         ratings.append("-")
        #         continue
        #     for r in rating_container.findAll('span'):
        #         if(int(r.text) >= 0 and int(r.text) <= 10):
        #             ratings.append(int(r.text))
        #             break
        #
        # # driver.quit()
        #
        # revs = dict(zip(user_names, zip(ratings, helpful_info, dates)))
        # items['data'] = revs
        # items['name'] = movie_name[0]
        # yield items

