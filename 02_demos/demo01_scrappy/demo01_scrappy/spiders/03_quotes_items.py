import scrapy
from demo01_scrappy.items import QuoteItem


class QuotesItemSpider(scrapy.Spider):
    name = "quotes_items"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.css("div.quote")

        for quote in quotes:
            # Instanciation d'un Item basé sur QuoteItem
            item = QuoteItem()
            # Remplissage des champs de l'item
            item['text'] = quote.css("span.text::text").get()
            item['author'] = quote.css("small.author::text").get()
            item['tags'] = quote.css("a.tag::text").getall()

            yield item

# commande pour lancer ce spider
# scrapy crawl quotes_items => infos dans le terminal
# scrapy crawl quotes_items -O outputs/quotes_items.json