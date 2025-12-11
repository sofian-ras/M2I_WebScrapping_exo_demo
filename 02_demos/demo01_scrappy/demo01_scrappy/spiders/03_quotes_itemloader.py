import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from demo01_scrappy.items import QuoteItem

def clean_text(value:str) -> str:
    return value.strip().replace("\n"," ")

class QuoteLoader(ItemLoader):
    default_output_processor = TakeFirst()

    tags_out = Join(", ")

    text_in = MapCompose(clean_text)

class QuotesItemsLoaderSpider(scrapy.Spider):
    name = "quotes_itemloader"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        quote_blocks = response.css("div.quote")

        for block in quote_blocks:
            loader = QuoteLoader(item=QuoteItem(),response=response,selector=block)
            loader.add_css("text", "span.text::text")
            loader.add_css("tags", "a.tag::text")
            loader.add_css("author_url", "span a::attr(href)")
            item = loader.load_item()

            yield item

# commande pour lancer ce spider
# scrapy crawl quotes_itemloader => infos dans le terminal
# scrapy crawl quotes_itemloader -O outputs/quotes_itemloader.json