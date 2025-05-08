import time
import json
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

app = FastAPI()

class URLRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get_html")
async def get_html(data: URLRequest):
    # Setup Chrome options
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument( '--headless' )
    options.add_argument( '--auto-open-devtools-for-tabs' )

    try:
        driver = uc.Chrome(options=options,driver_executable_path='/usr/local/bin/chromedriver')

        url = f"https://api.torob.com/v4/base-product/details/?prk={data.url}"

        driver.get(url)

        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "pre"))
        )

        script_content = element.get_attribute("innerHTML")

        data = json.loads(script_content)

        # Close the driver after fetching content
        driver.quit()

        # Return the HTML content as a response
        return data

    except Exception as e:
        return {"error": str(e)}
