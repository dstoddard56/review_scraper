import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

class ProductSearch:
    def __init__(self, product_name, nymag_url='https://nymag.com/strategist/article/{}.html'):
        self.product_name = product_name
        self.nymag_url = nymag_url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--incognito')
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.options)

<<<<<<< Updated upstream
    def data_search(self, url, selector):
        self.driver.get(url)
        source_code = self.driver.page_source
        soup = BeautifulSoup(source_code, 'html5lib')
        span_tag = soup.select_one(selector)

        if span_tag is not None:
            return span_tag.text.strip()
        else:
            print(f"Error: Element with selector '{selector}' not found on the page.")
            return None  # Or any other value or action you want to take in case of an error


    def nymag_search(self):
        nymag_product_name = self.data_search(self.nymag_url.format(self.product_name), 'a.product-buy-link span')
=======
    def data_search(self, url, xpath):
        try:
            self.driver.get(url)
            
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/section[6]/section[1]/article/section/div[1]/section[2]/div[2]/div[1]/div[1]"))) 
            soup = BeautifulSoup(source_code, 'html5lib')
            
            # Use the provided CSS selector to find the desired <div> element
            product_name = self.driver.find_element(By.XPATH, "/html/body/section[6]/section[1]/article/section/div[1]/section[2]/div[2]/div[1]/div[1]")
            
            # Now you can do something with the product_name_element
            if product_name_element:
                # Process or extract data from the selected element
                # For example, printing the text content of the element
                product_name = product_name_element.text.strip()
                return product_name
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def nymag_search(self):
        # Update the XPath based on the actual structure of the webpage
        xpath = "//div[@class='product-name']//a[@class='product-buy-link']//span"
        nymag_product_name = self.data_search(self.nymag_url.format(self.product_name), xpath)
>>>>>>> Stashed changes
        self.save_results(nymag_product_name)

    def save_results(self, product_name):
        df = pd.DataFrame({'Product Name': [product_name]})
        try:
            df.to_excel(r'C:\Users\12078\OneDrive\Desktop\product_list.xlsx', index=False)
            print("Data has been successfully saved to the Excel file.")
        except Exception as e:
<<<<<<< Updated upstream
            print(f"An error occurred: {e}")
        self.driver.quit()
=======
            print(f"An error occurred in save_results: {e}")
>>>>>>> Stashed changes

# Example usage:
user_input = input("Enter the product name: ")
product_search = ProductSearch(user_input)
product_search.nymag_search()

