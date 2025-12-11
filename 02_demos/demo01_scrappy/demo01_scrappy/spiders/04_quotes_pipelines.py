import scrapy
from demo01_scrappy.items import QuoteItem


class QuotesPipelinesSpider(scrapy.Spider):

    # Nom du spider utilisé dans la commande "crawl".
    name = "quotes_pipelines"

    # Domaine autorisé.
    allowed_domains = ["quotes.toscrape.com"]

    # URL de départ.
    start_urls = [
        "http://quotes.toscrape.com"
    ]

    def parse(self, response):

        for block in response.css("div.quote"):
            item = QuoteItem()

            item["text"] = block.css("span.text::text").get()
            item["author"] = block.css("small.author::text").get()
            item["tags"] = block.css("a.tag::text").getall()

            relative_author_url = block.css("span a::attr(href)").get()
            if relative_author_url:
                item["author_url"] = response.urljoin(relative_author_url)
            else:
                item["author_url"] = None

            # L'item est émis vers la chaîne de pipelines.
            yield item