import scrapy
from bookstore.items import BookItem
import re

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BookItem()
            item['title'] = book.css('h3 a::attr(title)').get()

            price_text = book.css('p.price_color::text').get()
            item['price'] = float(re.findall(r'[\d.]+', price_text)[0])

            rating_class = book.css('p.star-rating::attr(class)').get()
            rating_text = rating_class.split()[1]
            item['rating'] = self.rating_map.get(rating_text,0)

            availability = book.css('p.instock.availability::text').getall()
            item['availability'] = availability[1].strip() if len(availability) > 1 else 'unknow'


            yield item

        # Pagination sans page max
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page,callback=self.parse)


        # Pagination avec max 3 pages
        current_page = getattr(self,'page_count',0) + 1
        self.page_count = current_page

        if current_page < 3:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                yield response.follow(next_page,callback=self.parse)


# scrapy crawl books -O output/books.csv
# scrapy crawl books -O output/books.json