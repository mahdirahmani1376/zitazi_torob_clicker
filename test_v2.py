from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import json

# Setup Chrome options
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument( '--headless' )
options.add_argument( '--auto-open-devtools-for-tabs' )

driver = uc.Chrome(options=options,
# driver_executable_path='/usr/local/bin/chromedriver'
)

url = f"https://api.torob.com/v4/base-product/details/?prk=487ca2c3-d85f-4c3a-b36e-6734a3b00383"

driver.get(url)

html_content = driver.page_source
print(html_content)
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "pre"))
)

script_content = element.get_attribute("innerHTML")
data = json.loads(script_content)
print(data)
# Close the driver after fetching content
driver.quit()

