import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Replace 'your_product_name' with the actual product name
product_name = 'toasters'
nymag_url = f'https://nymag.com/strategist/article/best-{product_name}.html'

# Use requests to get the HTML content of the page
response = requests.get(nymag_url)
html_content = response.content

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'lxml')

# Find all span elements with a specific class or attribute that contains product information
# Adjust the class or attribute based on the structure of the HTML on the webpage
product_spans = soup.find_all('span')

# Print the product information
for span in product_spans:
    print(span.text.strip())
