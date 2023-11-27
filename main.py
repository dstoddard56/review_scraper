from bs4 import BeautifulSoup
import requests
from googlesearch import search
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import pandas as pd
import webbrowser

class ReviewScraper:
    def __init__(self, name, website):
        self.name = name
        self.website = website
        self.best_product = None
        self.product_price = None
        self.url = None

    def scrape(self, HTML_name_element, HTML_name_class, HTML_price_element, HTML_price_class, string = None):
        query = f"{self.website} best {self.name}"
        for url in search(query, tld="co.in", num=10, stop=1, pause=2):
            self.url = url

        response = requests.get(self.url)
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
        if self.url is not None:
            info += f"Link: {self.url}\n"

        return info

    def to_dict(self):
        return {
            'Name': self.name,
            'Website': self.website,
            'Best Product': self.best_product,
            'Product Price': self.product_price,
            'URL': self.url
        }

class NymagScraper(ReviewScraper):
    def scrape(self):
        super().scrape('div', 'product-name', 'span', 'product-buy-price')

class WirecutterScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', '_12e81b7a', 'div', '_24c5e6a6 product-pricebox-1')
'''
class BestProductsScraper(ReviewScraper):
    def scrape(self):
        query = f"{self.website} best {self.name}"
        for url in search(query, tld="co.in", num=10, stop=1, pause=2):
            self.url = url

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')

        product_name_element = soup.find('div', string='Best Overall')
        product_price_element = soup.find('div', class_='size-large css-1srh9ry e1a1omje0')

        if product_name_element:
            self.best_product = product_name_element.text.strip()

        if product_price_element:
            self.product_price = product_price_element.text.strip()
'''
class ForbesScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', 'finds-module-title', 'div', 'fbs-pricing__regular-price')

class CNETScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h4', 'c-bestListProductListing_hed g-text-bold', 'div', 'c-shortcodeListiclePrecapItem_button o-button o-button-small o-button-smallRound o-button-secondary')

        if self.best_product is None:
            super().scrape('h3', 'c-shortcodeListicle_hed g-text-medium g-outer-spacing-bottom-xsmall', 'div', 'c-shortcodeListiclePrecapItem_button o-button o-button-small o-button-smallRound o-button-primary')

class ProductSearch:
    def __init__(self, name):
        self.name = name
        self.review_scrapers = [
            WirecutterScraper(name, "Wirecutter"),
            #BestProductsScraper(name, "bestproducts.com"),
            ForbesScraper(name, "Forbes"),
            NymagScraper(name, "NY Mag"),
            CNETScraper(name, "CNET")
        ]

    def search(self):
        for scraper in self.review_scrapers:
            scraper.scrape()

    def store_results_as_dictionary(self):
        return [scraper.to_dict() for scraper in self.review_scrapers]

    def display_info(self):
        result = f"Product: {self.name}\n"
        for scraper in self.review_scrapers:
            result += scraper.display_info() + "\n"
        return result

class ProductSearchGUI:
    def __init__(self, master):
        style = ttk.Style()
        style.theme_use('alt')

        self.master = master
        master.title("Product Review Scraper")
        master.geometry("750x275")

        self.label = ttk.Label(master, text="Enter a product name:")
        self.label.pack()

        self.entry = ttk.Entry(master)
        self.entry.pack()
        self.entry.focus()

        self.result_text = tk.Text(master, height=10, width=100, wrap='word')
        self.result_text.pack()

        self.search_button = ttk.Button(master, text="Search", command=self.search_threading)
        self.search_button.pack()

        self.export_button = ttk.Button(master, text="Export Results", command=self.export_results)
        self.export_button.pack()

        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.pack()

    def export_results(self):
        product_name = self.entry.get()
        self.progress_bar.start()
        export_thread = threading.Thread(target=self.export_results_thread, args=(product_name,))
        export_thread.start()

    def export_results_thread(self, product_name):
        product_search = ProductSearch(product_name)
        product_search.search()
        results = product_search.store_results_as_dictionary()
        df = pd.DataFrame(results)
        df.to_csv('product_search_results.csv', mode='a', header=not os.path.exists('product_search_results.csv'), index=False)
        self.progress_bar.stop()
        self.master.after(0, self.update_export_button_text)

    def update_export_button_text(self):
        self.export_button.config(text="Results Exported")
        print("Results Exported")

    def search_threading(self):
        product_name = self.entry.get()
        self.progress_bar.start()
        search_thread = threading.Thread(target=self.search_and_display, args=(product_name,))
        search_thread.start()

    def search_and_display(self, product_name):
        product_search = ProductSearch(product_name)
        product_search.search()

        self.master.after(0, lambda: self.update_gui(product_search))

    def update_gui(self, product_search):
        self.progress_bar.stop()
        self.result_text.delete(1.0, tk.END)
        result_text = product_search.display_info()
        self.insert_hyperlinks(result_text)

    def insert_hyperlinks(self, text):
        lines = text.split('\n')
        for line in lines:
            if line.startswith("Link:"):
                link = line[6:]
                self.result_text.insert(tk.END, "Link: ", 'normal')
                self.result_text.insert(tk.END, link, 'link')
                self.result_text.insert(tk.END, "\n", 'normal')
            else:
                self.result_text.insert(tk.END, line + "\n", 'normal')

        self.result_text.tag_config('link', foreground='blue', underline=True)
        self.result_text.tag_bind('link', '<Button-1>', self.open_url)
        self.result_text.tag_bind('link', '<Enter>', lambda e: self.result_text.config(cursor="hand2"))
        self.result_text.tag_bind('link', '<Leave>', lambda e: self.result_text.config(cursor=""))

    def open_url(self, event):
        index = self.result_text.index(tk.CURRENT)
        start, end = index.split(".")
        start = f"{start}.0"
        clicked_text = self.result_text.get(start, f"{start} lineend")

        url = clicked_text[len("Link: "):].strip()

        webbrowser.open(url)

root = tk.Tk()
app = ProductSearchGUI(root)
root.mainloop()
