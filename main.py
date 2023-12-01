from bs4 import BeautifulSoup
import requests
from googlesearch import search
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import pandas as pd
import webbrowser
import os


#defining parent class
class ReviewScraper:
    def __init__(self, name, website):
        self.name = name
        self.website = website
        self.best_product = None
        self.product_price = None
        self.url = None
        
    #caching results in a dictionary 
    _cache = {}

    #scraping method makes google search of "{name of website} best {user-inputted product}" and returns the url of the first result
    def scrape(self, HTML_name_element, HTML_name_class, HTML_price_element, HTML_price_class, string = None):
        
        '''
        NOT WORKING
        #check cache for requested product
        if self.url in ReviewScraper._cache:
            print("Retreiving cached data for", self.url)
            result = ReviewScraper._cache[self.url]
            self.best_product = result['best_product']
            self.product_price = result['product_price']
            return
        '''
        
        query = f"{self.website} best {self.name}"
        for url in search(query, tld="co.in", num=10, stop=1, pause=2):
            self.url = url
            
        #requests receives the url and passes it to beautifulsoup to parse the HTML
        response = requests.get(self.url)
    
        #beautifulsoup takes the text of the response and parses it using lxml
        soup = BeautifulSoup(response.text, 'lxml')

        #bs4 finds the HTML element containing the product name and prices which is defined later in subclasses
        product_name_element = soup.find(HTML_name_element, class_=HTML_name_class)
        product_price_element = soup.find(HTML_price_element, class_=HTML_price_class)

        #if the product name element exists, grab the text and strip the formatting
        if product_name_element:
            self.best_product = product_name_element.text.strip()

        #same for price element
        if product_price_element:
            self.product_price = product_price_element.text.strip()
        
        #store scraped info in cache
        #ReviewScraper._cache[self.url] = {'best_product': self.best_product, 'product_price': self.product_price}
    
    #display info method displays the information found in the scrape method
    def display_info(self):
        #if the element is found, display the extracted information, else say no information was found on the given website
        info = ""
        if self.best_product is not None:
            first_line = self.best_product.split('\n')[0]
            info += f"Best {self.name} according to {self.website}: {first_line}\n"
        else:
            info += f"No information found on {self.website}\n"
            
        #repeat for product price element
        if self.product_price is not None:
            info += f"Price: {self.product_price}\n"
        else:
            info += "No price information available\n"
        if self.url is not None:
            info += f"Link: {self.url}\n"

        return info

    #throw extracted information into a dictionary
    def to_dict(self):
        return {
            'Product': self.name,
            'Website': self.website,
            'Best Product': self.best_product,
            'Product Price': self.product_price,
            'URL': self.url
        }

#subclasses for specific websites where the parameters for the scrape method are entered
class NymagScraper(ReviewScraper):
    def scrape(self):
        super().scrape('div', 'product-name', 'span', 'product-buy-price')

class WirecutterScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', '_908e815b e4c36628 bef5fbd9', 'div', '_6f5d0646 product-pricebox-0')
        

class BestProductsScraper(ReviewScraper):
    def scrape(self):
        super().scrape('div', 'css-1f1nsoy eyaokey2', 'div', '_6f5d0646 product-pricebox-0')


class ForbesScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h3', 'finds-module-title', 'div', 'embed-base finds-embed')
'''
class Underscored(ReviewScraper):
    def scrape(self):
        super().scrape('h3', 'cuisinart-chefs-convection-toaster-oven-tob-260n1', 'div', 'product-card__button-area')
'''
#this website's formatting is inconsistent, so if the first element is not found check the next
class CNETScraper(ReviewScraper):
    def scrape(self):
        super().scrape('h4', 'c-bestListProductListing_hed g-text-bold', 'div', 'c-shortcodeListiclePrecapItem_button o-button o-button-small o-button-smallRound o-button-secondary')

        if self.best_product is None:
            super().scrape('h3', 'c-shortcodeListicle_hed g-text-medium g-outer-spacing-bottom-xsmall', 'div', 'c-shortcodeListiclePrecapItem_button o-button o-button-small o-button-smallRound o-button-primary')

#product search class for conducting the web searches for each website
class ProductSearch:
    def __init__(self, name):
        self.name = name
        self.review_scrapers = [
            WirecutterScraper(name, "Wirecutter"),
            ForbesScraper(name, "Forbes"),
            NymagScraper(name, "NY Mag"),
            CNETScraper(name, "CNET"),
            BestProductsScraper(name, "bestproducts.com")
            #Underscored(name, "CNN")
        ]

    #method for searching for information with each scraper class
    def search(self):
        for scraper in self.review_scrapers:
            scraper.scrape()

    #stores scraper results in a list of dictionaries
    def store_results_as_dictionary(self):
        return [scraper.to_dict() for scraper in self.review_scrapers]

    #display the information found in each scraper class
    def display_info(self):
        result = f"Product: {self.name}\n"
        for scraper in self.review_scrapers:
            result += scraper.display_info() + "\n"
        return result

#class for the user interface
class ProductSearchGUI:
    def __init__(self, master):
        #setting GUI style to 'alt'
        style = ttk.Style()
        style.theme_use('alt')

        #initialize GUI window with specified title and size
        self.master = master
        master.title("Product Review Scraper")
        master.geometry("1000x600")

        #creates and packs a label for the user entry textbox
        self.label = ttk.Label(master, text="Enter a product name:")
        self.label.pack()
        
        '''
        self.message = ttk.Label(master, text="")
        self.message.pack()
        '''
        #user input is entered into an entry widget
        self.entry = ttk.Entry(master)
        self.entry.pack()
        #when the program is launched, the mouse gets focused into the entry widget
        self.entry.focus()

        #defining size and configuration of box where results are displayed
        self.result_text = tk.Text(master, height=30, width=150, wrap='word')
        self.result_text.pack()

        #defining "search" button. The button command runs the search_threading method
        self.search_button = ttk.Button(master, text="Search", command=self.search_threading)
        self.search_button.pack()

        #defining the "export results" button. The button command rusn the export_results method
        self.export_button = ttk.Button(master, text="Export Results", command=self.export_results)
        self.export_button.pack()

        #creating a progress bar at the bottom of the GUI window to demonstrate that the program is running
        #set to indeterminate because I don't know the exact time the program will take to complete
        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.pack()

    #exporting results to CSV
    def export_results(self):
        #grab product name
        product_name = self.entry.get()
        #run the progress bar
        self.progress_bar.start()
        #run threading method to export results in the background 
        export_thread = threading.Thread(target=self.export_results_thread, args=(product_name,))
        export_thread.start()

    #threading the export results method as to not freeze the GUI window
    def export_results_thread(self, product_name):
        #create instance of ProductSearch class using entered product name
        product_search = ProductSearch(product_name)
        #start the search for each scraper
        product_search.search()
        #store results in dictionary
        results = product_search.store_results_as_dictionary()
        #using a pandas DataFrame to format results before storing them in a CSV
        df = pd.DataFrame(results)
        df.to_csv('product_search_results.csv', mode='a', header=not os.path.exists('product_search_results.csv'), index=False)
        #stop the progress bar
        self.progress_bar.stop()
        #the text in the "export results" button is updated to "results exported" to show that the process is complete
        self.master.after(0, self.update_export_button_text)

    #updating "export results" button text to "results exported" for better user experience
    def update_export_button_text(self):
        self.export_button.config(text="Results Exported")
        print("Results Exported")

    #using a new thread for the search process as to not freeze the GUI window 
    def search_threading(self):
        product_name = self.entry.get()
        self.progress_bar.start()
        #self.update_message("Searching in progress...")
        search_thread = threading.Thread(target=self.search_and_display, args=(product_name,))
        search_thread.start()
    '''   
    def update_message(self, message):
        self.message.config(text=message)
    '''
    #make search and display results in GUI results window
    def search_and_display(self, product_name):
        product_search = ProductSearch(product_name)
        product_search.search()

        self.master.after(0, lambda: self.update_gui(product_search))

    #update GUI with results
    def update_gui(self, product_search):
        self.progress_bar.stop()
        #clears existing text in the results window. Good for making multiple searches/exports
        self.result_text.delete(1.0, tk.END)
        #get results and add hyperlinks for URLS
        result_text = product_search.display_info()
        self.insert_hyperlinks(result_text)

    #create hyperlinks for the URLs displayed in the results box
    def insert_hyperlinks(self, text):
        lines = text.split('\n')
        for line in lines:
            #check if the line starts with the word "Link:"
            #if it does, grab the URL from the line
            if line.startswith("Link:"):
                link = line[6:]
                #display "Link:" in the URL line as normal text and display the URL as a hyperlink
                self.result_text.insert(tk.END, "Link: ", 'normal')
                self.result_text.insert(tk.END, link, 'link')
                self.result_text.insert(tk.END, "\n", 'normal')
            else:
                self.result_text.insert(tk.END, line + "\n", 'normal')

        #formatting the hyperlink
        self.result_text.tag_config('link', foreground='blue', underline=True)
        
        #events for interacting with the hyperlink. Cursor turns into a hand for better user experience
        self.result_text.tag_bind('link', '<Button-1>', self.open_url)
        self.result_text.tag_bind('link', '<Enter>', lambda e: self.result_text.config(cursor="hand2"))
        self.result_text.tag_bind('link', '<Leave>', lambda e: self.result_text.config(cursor=""))

    #if the user clicks on the hyperlink, launch a browser with the clicked URL
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