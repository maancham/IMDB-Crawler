# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import Main_page, Rating_page, Review_page


class RatingsSpider(scrapy.Spider):
    name = 'ratings'
    allowed_domains = ['imdb.com']
    with open(r"C:\Users\hoomo\Desktop\bahrak_data\scrapy\first\first\ratings.txt", "rt") as f:
        start_urls = [url.strip() for url in f.readlines()]

    def parse(self, response):
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