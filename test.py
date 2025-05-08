from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome
chromeOptions = Options()
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chromeOptions)

# Open the URL first
url = 'https://torob.com/p/96693172-2855-41e2-b03a-4b800383aef2/...'
driver.get(url)

# Wait for page to fully load before interacting
time.sleep(10)  # you can tweak this if necessary

# Switch to iframe
iframe = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe"))
)
driver.switch_to.frame(iframe)

# # Wait for the checkbox to be clickable and then click
checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type=checkbox]"))
)
checkbox.click()
#
# print("Checkbox clicked!")

# Optional: close driver after you're done
# driver.quit()
