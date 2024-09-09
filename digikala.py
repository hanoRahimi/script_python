from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get('https://www.digikala.com/search/category-mobile-phone/product-list/')

time.sleep(5)

products = driver.find_elements(By.CLASS_NAME, 'styles_VerticalProductCard__productTitle__6zjjN')
prices = driver.find_elements(By.XPATH, "//span[@data-testid='price-final']")

for i in range(len(products)):
    title = products[i].text
    price = prices[i].text
    print(f'model: {title}, price: {price}')


driver.quit()
