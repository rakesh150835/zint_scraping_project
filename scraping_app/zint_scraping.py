import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chrome_options = Options()
#chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

driver.get("https://app.zint.io/login")

email_input = driver.find_element(By.NAME, 'email')  # Adjust the name as needed
password_input = driver.find_element(By.NAME, 'password')  # Adjust the name as needed

email_input.send_keys('Rory.fitzmaurice@inxpress.com')
password_input.send_keys('Grannyfitz1')

button = driver.find_element(By.CSS_SELECTOR, 'button.basic-button-base.button-dark.full-width')
driver.execute_script("arguments[0].click();", button)

time.sleep(15)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "table"))  # Replace with the appropriate selector
)

# Locate the table
table = driver.find_element(By.CSS_SELECTOR, "table")

rows = table.find_elements(By.TAG_NAME, "tr")
if rows:
    print("rows found")
else:
    print("rows not found")


