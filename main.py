from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime

# Importing from other files
from db import create_db
from db import insert_data
from xpaths import ALLOW_COOKIES_XPATH, YEAR

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
    from_airport = input(
        "Enter the 3-letter airport code you're flying from, ex BUH: "
    ).upper()
    while len(from_airport) != 3 or not from_airport.isalpha():
        print("Invalid format. Please try again.")
        from_airport = input("Enter departure airport code: ").upper()
    to_airport = input("Enter arrival airport code: ").upper()
    while len(to_airport) != 3 or not to_airport.isalpha():
        print("Invalid format. Please try again.")
        to_airport = input("Enter arrival airport code: ").upper()

    # Adjusted to use YEAR constant for departure date
    departure_month_day = input("Enter departure month and day (MM-DD): ")
    while not validate_date(f"{YEAR}-{departure_month_day}"):
        print("Invalid format. Please try again.")
        departure_month_day = input("Enter departure month and day (MM-DD): ")
    departure_date = f"{YEAR}-{departure_month_day}"

    # Adjusted to use YEAR constant for return date
    return_month_day = input("Enter return month and day (MM-DD): ")
    while not validate_date(f"{YEAR}-{return_month_day}"):
        print("Invalid format. Please try again.")
        return_month_day = input("Enter return month and day (MM-DD): ")
    return_date = f"{YEAR}-{return_month_day}"

    url_to_manipulate = base_url.format(
        from_airport, to_airport, departure_date, return_date
    )
    driver.get(url_to_manipulate)

    return from_airport, to_airport, departure_date, return_date


def get_flight_data(driver):
    # get the price
    price_xpath = "/html/body/div[1]/div[3]/div/div/div[2]/ith-tab-filters/div/ith-tab-filter[1]/div/strong[1]/span"
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, price_xpath))
    )
    price = price_element.text
    print(f"Price: {price} RON 💸")

    # get the departure hour
    departure_xpath = "/html/body/div[1]/div[3]/div/div/div[2]/ith-flight-offers/div/div[1]/div/div/ith-flight-offer/div/div/div[1]/ith-flight-stage[1]/div/div[2]/div/div[1]/div[1]/div[1]/span"
    departure_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, departure_xpath))
    )
    departure_hour = departure_element.text
    print(f"Departure hour: {departure_hour}")

    # get the return hour
    return_hour_xpath = "/html/body/div[1]/div[3]/div/div/div[2]/ith-flight-offers/div/div[1]/div/div/ith-flight-offer/div/div/div[1]/ith-flight-stage[2]/div/div[2]/div/div[1]/div[1]/div[1]/span"
    return_hour_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, return_hour_xpath))
    )
    return_hour = return_hour_element.text
    print(f"Return hour: {return_hour}")

    return price, departure_hour, return_hour


def run_again():
    run_again = input("Do you want to run the program again? (y/n): ")
    if run_again.lower() in {"yes", "y"}:
        main()
    else:
        print("👋 Goodbye! 👋")


def main():
    allow_cookies(driver)
    from_airport, to_airport, departure_date, return_date = navigate(driver)
    price, departure_hour, return_hour = get_flight_data(driver)
    print("🚀 Program finished, please check your browser.")
    create_db()
    insert_data(
        from_airport,
        to_airport,
        departure_date,
        return_date,
        price,
        departure_hour,
        return_hour,
    )
    run_again()


if __name__ == "__main__":
    main()
