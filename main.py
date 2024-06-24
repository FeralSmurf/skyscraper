from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

from xpaths import ALLOW_COOKIES_XPATH

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.get("https://vola.ro/")
wait = WebDriverWait(driver, 3)  # Define the wait variable


def allow_cookies(driver):
    try:
        allow_cookies_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, ALLOW_COOKIES_XPATH))
        )
        allow_cookies_element.click()
        print("🙂 Button clicked, cookies allowed 🍪.")
        return True
    except Exception as e:
        print(f"No button found. Details: {e}")
        return False


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def navigate(driver):
    base_url = (
        "https://www.vola.ro/flight_search/from_code/{}/to_code/{}/dd/{}/rd/{}/ad/1"
    )
    from_airport = input("Enter the 3-letter airport code you're flying from, ex BUH: ").upper()
    while len(from_airport) != 3 or not from_airport.isalpha():
        print("Invalid format. Please try again.")
        from_airport = input("Enter departure airport code: ").upper()
    to_airport = input("Enter arrival airport code: ").upper()
    while len(to_airport) != 3 or not to_airport.isalpha():
        print("Invalid format. Please try again.")
        to_airport = input("Enter arrival airport code: ").upper()
    departure_date = input("Enter departure date (YYYY-MM-DD): ")
    while not validate_date(departure_date):
        print("Invalid format. Please try again.")
        departure_date = input("Enter departure date (YYYY-MM-DD): ")
    return_date = input("Enter return date (YYYY-MM-DD): ")
    while not validate_date(return_date):
        print("Invalid format. Please try again.")
        return_date = input("Enter return date (YYYY-MM-DD): ")
    url_to_manipulate = base_url.format(
        from_airport, to_airport, departure_date, return_date
    )
    driver.get(url_to_manipulate)


if __name__ == "__main__":
    allow_cookies(driver)
    navigate(driver)
    print("🚀 Program finished, please check your browser.")
