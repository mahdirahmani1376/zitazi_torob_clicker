import time
from datetime import datetime, timedelta
import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging
import sys
from bs4 import BeautifulSoup
import json
import mysql.connector
from dotenv import load_dotenv
from sqlalchemy import create_engine

########################
# database connection
########################
load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

# Create an SQLAlchemy connection string
# connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_database}'

# Create an SQLAlchemy engine
# engine = create_engine(connection_string)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    database="zitazi",
    unix_socket="/var/run/mysqld/mysqld.sock"  # Adjust this path if needed
)
df = pd.read_sql('SELECT * FROM torob_products where clickable = 1', conn)
print(df)
sys.exit()


########################
# logging configurations
########################
now = datetime.now()
logFolder = 'logs'
if not os.path.exists('logs'):
    os.makedirs(logFolder)

programTimeFormat = now.strftime('%Y-%m-%d-%H-%M-%S')
logFileName = os.path.join(logFolder, f"{programTimeFormat}.log")
logging.basicConfig(
    filename=logFileName,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d-%H-%M-%S',
    level=logging.INFO,
    encoding="UTF-8"
)
########################
# configs for chrome driver
########################
sleepTime = 2
chromeOptions = Options()
chrome_options.add_argument("--headless")  # Run without UI
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Required for running as root
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid /dev/shm issues
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chromeOptions)
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chromeOptions)

print('program started ')
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

for i in df.itertuples():
    try:
        urlToCLick = i[df.columns.get_loc('web_client_absolute_url') + 1]
        with requests.Session() as s:
            driver.get(urlToCLick)
            successfulResponseMessage = f"""
            successfully visited {urlToCLick} 
            sleeping for {sleepTime} seconds
            """
            print(successfulResponseMessage)
            logging.info(successfulResponseMessage)
            time.sleep(sleepTime)
    except Exception as e:
        print(f"error occurred in program with message: {e}")
        logging.error("Exception occurred", exc_info=True)