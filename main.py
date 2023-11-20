from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class ProductSearch:
    def __init__(self, product_name, nymag_url='https://nymag.com/strategist/article/best-{}.html'):
        self.product_name = product_name
        self.nymag_url = nymag_url

    def data_search(self, url, xpath):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run Chrome in headless mode
            options.add_argument('--incognito')
            options.add_argument('--ignore-certificate-errors')
            
            with webdriver.Chrome(options=options) as driver:
                driver.get(url)

                # Wait for the element to be located
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

                # Use the provided XPath
                product_name_element = driver.find_element(By.XPATH, xpath)

                if product_name_element:
                    # Process or extract data from the selected element
                    # For example, printing the text content of the element
                    product_name = product_name_element.text.strip()
                    return product_name
        except TimeoutException:
            print("Timed out waiting for the element to be located.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def nymag_search(self):
        # Update the XPath based on the actual structure of the webpage
        xpath = '/html/body/section[6]/section[1]/article/section/div[1]/section[2]/div[2]/div[1]/div[1]'
        nymag_product_name = self.data_search(self.nymag_url.format(self.product_name), xpath)
        if nymag_product_name:
            self.save_results(nymag_product_name)

    def save_results(self, product_name):
        try:
            df = pd.DataFrame({'Product Name': [product_name]})
            df.to_excel(r'C:\Users\derek\OneDrive\Desktop\product_list.xlsx', index=False)
            print("Data has been successfully saved to the Excel file.")
        except Exception as e:
            print(f"An error occurred in save_results: {e}")

# Example usage:
user_input = input("Enter the product name: ")
product_search = ProductSearch(user_input)
product_search.nymag_search()
