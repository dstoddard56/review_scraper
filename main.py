from bs4 import BeautifulSoup
from googlesearch import search
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, END, Text
#from openpyxl import Workbook
#import os

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
        info = ""
        if self.best_product is not None:
            first_line = self.best_product.split('\n')[0]
            info += f"According to {self.website}: {first_line}\n"
        else:
            info += f"No information found on {self.website}\n"

        if self.product_price is not None:
            info += f"Price: {self.product_price}\n"
        else:
            info += "No price information available\n"

        return info

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

class CNETScraper(ReviewScraper):
    def scrape(self):
        super().scrape('div', 'c-shortcodeListiclePrecapItem_title g-text-xxsmall u-inline', 'div', 'c-shortcodeListiclePrecapItem_button o-button o-button-small o-button-smallRound o-button-secondary')

class ProductSearch:
    def __init__(self, name):
        self.name = name
        self.wirecutter_scraper = WirecutterScraper(name, "Wirecutter")
        self.best_products_scraper = BestProductsScraper(name, "bestproducts.com")
        self.forbes_scraper = ForbesScraper(name, "Forbes")
        self.nymag_scraper = NymagScraper(name, "NY Mag")
        self.cnet_scraper = CNETScraper(name, "CNET")

    def search(self):
        self.wirecutter_scraper.scrape()
        self.best_products_scraper.scrape()
        self.forbes_scraper.scrape()
        self.nymag_scraper.scrape()
        self.cnet_scraper.scrape()

    def get_display_info(self):
        result = f"Product: {self.name}\n"
        result += self.wirecutter_scraper.display_info() + "\n"
        result += self.best_products_scraper.display_info() + "\n"
        result += self.forbes_scraper.display_info() + "\n"
        result += self.nymag_scraper.display_info() + "\n"
        result += self.cnet_scraper.display_info()
        return result

class ProductSearchGUI:
    def __init__(self, master):
        self.master = master
        master.title("Product Review Scraper")

        master.geometry("500x250")

        self.label = Label(master, text="Enter a product name:")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()

        self.result_text = Text(master, height=10, width=85)
        self.result_text.pack()

        self.search_button = Button(master, text="Search", command=self.search_and_display)
        self.search_button.pack()

    def search_and_display(self):
        product_name = self.entry.get()
        product_search = ProductSearch(product_name)
        product_search.search()

        #Clear previous results
        self.result_text.delete(1.0, tk.END)

        # Display results in the Text widget
        result_text = product_search.get_display_info()
        self.result_text.insert(tk.END, result_text)

        '''
        self.write_to_excel(product_name, result_text, r'C:\Users\12078\OneDrive\Documents')
        '''
        
# Create the main window
root = tk.Tk()
app = ProductSearchGUI(root)

# Run the Tkinter event loop
root.mainloop()
