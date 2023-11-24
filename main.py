import requests
from bs4 import BeautifulSoup
from googlesearch import search

class ReviewScraper:
    def __init__(self, name, website):
        self.name = name
        self.website = website
        self.best_product = None
        self.product_price = None

    def scrape(self, HTML_name_element, HTML_name_class, HTML_price_element, HTML_price_class):
        query = f"{self.website} best {self.name}"

        for url in search(query, tld="co.in", num=10, stop=1, pause=2):
            _url = url

        response = requests.get(_url)
        soup = BeautifulSoup(response.text, 'lxml')

        product_name_element = soup.find(HTML_name_element, class_=HTML_name_class)
        product_price_element = soup.find(HTML_price_element, class_=HTML_price_class)

        if product_name_element:
            self.best_product = product_name_element.text.strip()

        if product_price_element:
            self.product_price = product_price_element.text.strip()

    def display_info(self):
        if self.best_product is not None:
            first_line = self.best_product.split('\n')[0]
            according_line = f"According to {self.website}: {first_line}"
            print(according_line)
        else:
            print(f"No information found on {self.website}")
        if self.product_price is not None:
            print(f"Price: {self.product_price}")
        else:
            print("No price information available")

class NymagScraper(ReviewScraper):
    def scrape(self):
        super().scrape('div', 'product-name', 'span', 'product-buy-price')

class WirecutterScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', '_12e81b7a', 'div', '_24c5e6a6 product-pricebox-1')

class BestProductsScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h2', 'css-1s0pzvh e8seki10', 'div', 'size-large css-1srh9ry e1a1omje0')

class ForbesScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', 'finds-module-title', 'div', 'fbs-pricing__regular-price')

class ProductSearch:
    def __init__(self, name):
        self.name = name
        self.wirecutter_scraper = WirecutterScraper(name, "Wirecutter")
        self.best_products_scraper = BestProductsScraper(name, "bestproducts.com")
        self.forbes_scraper = ForbesScraper(name, "forbes")
        self.nymag_scraper = NymagScraper(name, "NY Mag")

    def search(self):
        self.wirecutter_scraper.scrape()
        self.best_products_scraper.scrape()
        self.forbes_scraper.scrape()
        self.nymag_scraper.scrape()

    def display_info(self):
        print(f"Product: {self.name}")
        self.wirecutter_scraper.display_info()
        self.best_products_scraper.display_info()
        self.forbes_scraper.display_info()
        self.nymag_scraper.display_info()

product_name = input("Enter a product name: ")
product_search = ProductSearch(product_name)
product_search.search()
product_search.display_info()
