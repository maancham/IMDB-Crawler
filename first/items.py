# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Main_page(scrapy.Item):
    # define the fields for your item here like:
    movie_id = scrapy.Field()
    name = scrapy.Field()
    org_name = scrapy.Field()
    title_year = scrapy.Field()
    point = scrapy.Field()
    point_volume = scrapy.Field()
    user_reviews = scrapy.Field()
    critic_reviews = scrapy.Field()
    metascore = scrapy.Field()
    date = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    cast = scrapy.Field()
    story_line = scrapy.Field()
    plt_keywords = scrapy.Field()
    budget = scrapy.Field()
    users = scrapy.Field()
    genres = scrapy.Field()
    world_gross = scrapy.Field()
    usa_gross = scrapy.Field()
    runtime = scrapy.Field()
    production_companies = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    # pass

class Mini_page(scrapy.Item):
    movie_id = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    links = scrapy.Field()
    # pass

class Cast_page(scrapy.Item):
    movie_id = scrapy.Field()
    casts = scrapy.Field()
    casts_id = scrapy.Field()
    # pass

class Keyword_page(scrapy.Item):
    movie_id = scrapy.Field()
    keywords = scrapy.Field()
    keywords_relevance = scrapy.Field()
    # pass

class Rating_page(scrapy.Item):
    movie_id = scrapy.Field()
    name = scrapy.Field()

    tens_count = scrapy.Field()
    nines_count = scrapy.Field()
    eights_count = scrapy.Field()
    sevens_count = scrapy.Field()
    sixes_count = scrapy.Field()
    fives_count = scrapy.Field()
    fours_count = scrapy.Field()
    threes_count = scrapy.Field()
    twos_count = scrapy.Field()
    ones_count = scrapy.Field()

    tens_percent = scrapy.Field()
    nines_percent = scrapy.Field()
    eights_percent = scrapy.Field()
    sevens_percent = scrapy.Field()
    sixes_percent = scrapy.Field()
    fives_percent = scrapy.Field()
    fours_percent = scrapy.Field()
    threes_percent = scrapy.Field()
    twos_percent = scrapy.Field()
    ones_percent = scrapy.Field()

    all_average = scrapy.Field()
    minor_average = scrapy.Field()
    young_average = scrapy.Field()
    adult_average = scrapy.Field()
    senior_average = scrapy.Field()

    all_count = scrapy.Field()
    minor_count = scrapy.Field()
    young_count = scrapy.Field()
    adult_count = scrapy.Field()
    senior_count = scrapy.Field()

    male_all_average = scrapy.Field()
    male_minor_average = scrapy.Field()
    male_young_average = scrapy.Field()
    male_adult_average = scrapy.Field()
    male_senior_average = scrapy.Field()

    male_all_count = scrapy.Field()
    male_minor_count = scrapy.Field()
    male_young_count = scrapy.Field()
    male_adult_count = scrapy.Field()
    male_senior_count = scrapy.Field()

    female_all_average = scrapy.Field()
    female_minor_average = scrapy.Field()
    female_young_average = scrapy.Field()
    female_adult_average = scrapy.Field()
    female_senior_average = scrapy.Field()

    female_all_count = scrapy.Field()
    female_minor_count = scrapy.Field()
    female_young_count = scrapy.Field()
    female_adult_count = scrapy.Field()
    female_senior_count = scrapy.Field()

    top_thousand_average = scrapy.Field()
    top_thousand_count = scrapy.Field()
    us_users_average = scrapy.Field()
    us_users_count = scrapy.Field()
    non_us_users_average = scrapy.Field()
    non_us_users_count = scrapy.Field()

    # pass



class Review_page(scrapy.Item):
    movie_id = scrapy.Field()
    user_id = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
    # pass
