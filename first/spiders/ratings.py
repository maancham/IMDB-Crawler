# -*- coding: utf-8 -*-
import scrapy
import numpy as np
from bs4 import BeautifulSoup
from ..items import Rating_page
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

class RatingsSpider(scrapy.Spider):
    name = 'ratings'
    with open(r"ratings.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    # start_urls = start_urls[441871:]

    def parse(self, response):
        if not "No Ratings Available" in response.css('div.sectionHeading::text').extract():
            items = Rating_page()
            soup = BeautifulSoup(response.body, 'html5lib')
            containers = response.css('table')
            full_url_list = response.request.url.split("/")
            items['movie_id'] = full_url_list[4]

            header = response.css('h3')[0]
            movie_name = header.css('a::text').extract()
            items['name'] = movie_name[0]


            var_names = ['tens', 'nines', 'eights', 'sevens', 'sixes',
                         'fives', 'fours', 'threes', 'twos', 'ones' ]
            count_list = []
            percentage_list = []
            charts_container = containers[0]
            charts = charts_container.css('tr')
            for i in range(len(charts)):
                if (i == 0):
                    continue
                else:
                    elements = charts[i].css('td')
                    percentange_container = charts[i].css('div.topAligned::text')
                    if (len(percentange_container) == 0):
                        percentage_list.append(0)
                    else:
                        value = percentange_container.extract()[0].strip()
                        value = value[:-1]
                        percentage_list.append(float(value))

                    count_container = elements[len(elements) - 1]
                    count = count_container.css('div.leftAligned::text').extract_first()
                    count_list.append(locale.atoi(count))

            for i in range(10):
                count_tag = var_names[i] + '_count'
                percent_tag = var_names[i] + '_percent'
                items[count_tag] = count_list[i]
                items[percent_tag] = percentage_list[i]




            demo_container = containers[1]
            demos = demo_container.css('tr')
            demos = demos[1:]
            for j in range(3):
                all_demos = demos[j]
                prefix = ''
                if (j == 1):
                    prefix = 'male_'
                elif (j == 2):
                    prefix = 'female_'
                first_row_tables = all_demos.css('td.ratingTable')
                first_row_dict = {0: 'all', 1:'minor', 2:'young', 3:'adult', 4:'senior'}
                for i in range(len(first_row_tables)):
                    box = first_row_tables[i]
                    item_tag = first_row_dict[i]
                    bigcell_cont = box.css('div.bigcell::text')
                    smallcell_cont = box.css('div.smallcell')
                    if (len(smallcell_cont) == 0):
                        pass
                        items[prefix + item_tag + '_average'] = np.nan
                        items[prefix + item_tag + '_count'] = 0
                    else:
                        big_value = float(bigcell_cont.extract_first())
                        small_value = locale.atoi(smallcell_cont.css('a::text').extract_first())
                        items[prefix + item_tag + '_average'] = big_value
                        items[prefix + item_tag + '_count'] = small_value



            extra_container = containers[2]
            extra_first_row = extra_container.css('tr')[1]
            value_conts = extra_first_row.css('td')
            for i in range(3):
                if (i == 0):
                    avg_tag = 'top_thousand_average'
                    cnt_tag = 'top_thousand_count'
                elif (i == 1):
                    avg_tag = 'us_users_average'
                    cnt_tag = 'us_users_count'
                elif (i == 2):
                    avg_tag = 'non_us_users_average'
                    cnt_tag = 'non_us_users_count'

                target_cont = value_conts[i]
                bigcell_cont = target_cont.css('div.bigcell::text')
                smallcell_cont = target_cont.css('div.smallcell')
                if (len(smallcell_cont) == 0):
                    items[avg_tag] = np.nan
                    items[cnt_tag] = 0
                else:
                    big_value = float(bigcell_cont.extract_first())
                    small_value = locale.atoi(smallcell_cont.css('a::text').extract_first())
                    items[avg_tag] = big_value
                    items[cnt_tag] = small_value










            yield items