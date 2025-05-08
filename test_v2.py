from selenium import webdriver
import undetected_chromedriver as uc
import time

# Setup Chrome options
options = uc.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument( '--headless' )
# options.add_argument( '--auto-open-devtools-for-tabs' )

# Launch the Chrome browser
# Launch the Chrome browser
driver = uc.Chrome(options=options)

url = f"https://api.torob.com/v4/base-product/details/?prk=487ca2c3-d85f-4c3a-b36e-6734a3b00383"
# Fetch the page
driver.get(data.url)

# Wait for the page to load (you can adjust the sleep time or use WebDriverWait)
time.sleep(5)

# Get the page source (HTML content)
html_content = driver.page_source
data = json.loads(script_content)['products_info']['result']

# Close the driver after fetching content
driver.quit()

