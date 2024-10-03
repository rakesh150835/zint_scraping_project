from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .models import Company_Details
from dotenv import load_dotenv
import os

load_dotenv()

ZINT_EMAIL = os.getenv('ZINT_EMAIL')
ZINT_PASSWORD = os.getenv('ZINT_PASSWORD')

# get next pagination button 
def get_pagination_button(driver):
    try:
        divs = driver.find_elements(By.CSS_SELECTOR, ".col-md-auto.col-1.pagination-button")
        last_div = divs[-1]
        button = last_div.find_element(By.TAG_NAME, "button")
        
        if button.is_enabled():
            button.click()
            get_page_data(driver)
        else:
            print("No more pages to navigate")
        
    except Exception as e:
        print(f"Error getting pagination button: {e}")


# get page data
def get_page_data(driver):
    try:
        time.sleep(15)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))  # Replace with the appropriate selector
        )
        # Locate the table
        tables = driver.find_elements(By.CSS_SELECTOR, ".table.table-striped.table-bordered.company-results-table")

        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
        )
        # # get table headings
        # headings = tables[0].find_elements(By.TAG_NAME, "th")
        # print(headings)

        second_table = tables[1]
        rows = second_table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            # print(len(row_data))
            print(row_data[1])
            if len(row_data) < 11:
                print("skipping row")
                continue

            company_details = Company_Details(
                company_name=row_data[1],
                email=row_data[2],
                registered_address_town=row_data[3],
                url=row_data[4],
                company_summary=row_data[5],
                revenue=row_data[6],
                registered_address_postcode=row_data[8],
                linkedin_url=row_data[9],
                do_not_contact_status=True if row_data[10] == 'Do Not Contact' else False,
            )
            company_details.save()

        get_pagination_button(driver)

    except Exception as e:
        print(f"Error getting page data: {e}")


# login to zint 
def login(driver):
    try:
        driver.get("https://app.zint.io/login")

        email_input = driver.find_element(By.NAME, 'email')  
        password_input = driver.find_element(By.NAME, 'password')  

        email_input.send_keys(ZINT_EMAIL)
        password_input.send_keys(ZINT_PASSWORD)

        button = driver.find_element(By.CSS_SELECTOR, 'button.basic-button-base.button-dark.full-width')
        driver.execute_script("arguments[0].click();", button)

        get_page_data(driver)

    except Exception as e:
        print(f"Error logging in: {e}")


def scrape_data():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    login(driver)

    driver.quit()


#scrape_data()



