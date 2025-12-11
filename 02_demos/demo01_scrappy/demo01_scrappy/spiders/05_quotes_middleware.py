import scrapy


class QuotesMiddlewareSpider(scrapy.Spider):

     # Nom du spider utilisé avec la commande "crawl".
    name = "quotes_middleware"

    # Domaine autorisé.
    allowed_domains = ["quotes.toscrape.com"]

    # URL de départ.
    start_urls = [
        "http://quotes.toscrape.com"
    ]



    def parse(self, response):

        # Récupération du User-Agent utilisé pour cette requête.
        user_agent_bytes = response.request.headers.get("User-Agent", b"")
        user_agent = user_agent_bytes.decode("utf-8", errors="ignore")


        yield {
            "page_url": response.url,
            "user_agent": user_agent,
        }


        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)