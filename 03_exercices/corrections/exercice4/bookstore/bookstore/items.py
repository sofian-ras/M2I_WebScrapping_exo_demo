# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookstoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 3. Définir un `BookItem` avec : title, price, rating, availability

class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()