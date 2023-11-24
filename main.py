import requests  
from bs4 import BeautifulSoup
from googlesearch import search

class ReviewScraper:
    def __init__(self, name, website):
        self.name = name
        self.website = website
        self.best_product = None
        self.product_price = None

    def scrape(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def display_info(self):
        if self.best_product is not None:
            first_line = self.best_product.split('\n')[0]
            print(f"According to {self.website}: {first_line}")
        else:
            print(f"No information found on {self.website}")
        if self.product_price is not None:
            print(f"Price: {self.product_price}")
        else:
            print("No price information available")

class NymagScraper(ReviewScraper):
    def scrape(self):
        nymag_url = f'https://nymag.com/strategist/article/best-{self.name}.html'
        response = requests.get(nymag_url)
        soup = BeautifulSoup(response.text, 'lxml')

        product_name_element = soup.find('div', class_='product-name')
        product_price_element = soup.find('span', class_='product-buy-price')

        if product_name_element:
            self.best_product = product_name_element.text.strip()

        if product_price_element:
            self.product_price = product_price_element.text.strip()

class WirecutterScraper(ReviewScraper):
    def scrape(self):
        query = f"wirecutter best {self.name}"

        for url in search(query, tld="co.in", num=10, stop=1, pause=2):
            wirecutter_url = url

        response = requests.get(wirecutter_url)
        soup = BeautifulSoup(response.text, 'lxml')

        product_name_element = soup.find('h3', class_='d73f30a8 _12e81b7a _18247845')
        product_price_element = soup.find('div', class_='_24c5e6a6 product-pricebox-1')

        if product_name_element:
            self.best_product = product_name_element.text.strip()

        if product_price_element:
            self.product_price = product_price_element.text.strip()

class ProductSearch:
    def __init__(self, name):
        self.name = name
        self.nymag_scraper = NymagScraper(name, "NY Mag")
        self.wirecutter_scraper = WirecutterScraper(name, "Wirecutter")

    def search(self):
        self.nymag_scraper.scrape()
        self.wirecutter_scraper.scrape()

    def display_info(self):
        print(f"Product: {self.name}")
        self.nymag_scraper.display_info()
        self.wirecutter_scraper.display_info()

product_name = input("Enter a product name: ")
product_search = ProductSearch(product_name)
product_search.search()
product_search.display_info()
