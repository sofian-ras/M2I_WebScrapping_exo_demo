import scrapy


class QuotesPaginationSpider(scrapy.Spider):
    name = "quotes_pagination"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quotes = response.css("div.quote")

        for quote in quotes:
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("a.tag::text").getall()

            yield {
                "text" : text,
                "author" : author,
                "tags" : tags,
                "page_url" : response.url
            }
        
        next_page = response.css("li.next a::attr(href)").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

# commande pour lancer ce spider
# scrapy crawl quotes_pagination => infos dans le terminal
# scrapy crawl quotes_pagination -O outputs/quotes_pagination.json