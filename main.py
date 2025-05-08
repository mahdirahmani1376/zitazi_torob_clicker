from fastapi import FastAPI
from selenium import webdriver
import undetected_chromedriver as uc
from pydantic import BaseModel
import time
from fastapi.responses import HTMLResponse

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
        # Launch the Chrome browser
        # Launch the Chrome browser
        driver = uc.Chrome(options=options)

        url = f"https://api.torob.com/v4/base-product/details/?prk={data.url}"
        # Fetch the page
        driver.get(data.url)
        driver.save_screenshot("screenshot.png")

        # Wait for the page to load (you can adjust the sleep time or use WebDriverWait)
        time.sleep(5)

        # Get the page source (HTML content)
        html_content = driver.page_source
        data = json.loads(script_content)['products_info']['result']

        # Close the driver after fetching content
        driver.quit()

        # Return the HTML content as a response
        return HTMLResponse(content=html_content)

    except Exception as e:
        return {"error": str(e)}
