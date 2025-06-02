import time
from datetime import datetime, timedelta
import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import sys
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

########################
# configs for chrome driver
########################
chromeOptions = Options()
chromeOptions.add_argument("--headless")  # Run without UI
chromeOptions.add_argument("--disable-gpu")  # Disable GPU acceleration
chromeOptions.add_argument("--no-sandbox")  # Required for running as root
chromeOptions.add_argument("--disable-dev-shm-usage")  # Avoid /dev/shm issues
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chromeOptions)

print('program started ')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

response = requests.get('http://localhost:80/api/amazon-list').text
df = pd.DataFrame(json.loads(response)['data'])
for i in df.itertuples():
    try:
        urlToCLick = i[2]
        id = i[1]
        driver.get(urlToCLick)

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        stock = 88
        stockElement = driver.find_elements(By.CSS_SELECTOR, "div#outOfStock")
        if stockElement:
            stock = 0

        price = None
        priceElement = driver.find_elements(By.CSS_SELECTOR, "div.twister-plus-buying-options-price-data")
        if priceElement:
            price = json.loads(priceElement[0].get_attribute('innerHTML'))['desktop_buybox_group_1'][0]['priceAmount']

        if price is None:
            stock = 0

        body = {
            'price' : price,
            'stock' : stock,
        }

        headers = {
            'accept' : 'application/json'
        }

        responseUpdate = requests.put(f'http://localhost:80/api/variations/{id}/update',params = body , headers = headers)

    except Exception as e:
        print(f"error occurred in program with message: {e}")
