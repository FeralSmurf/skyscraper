from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import re

# Importing from other files
from db import create_db, insert_data
from xpaths import ALLOW_COOKIES_XPATH
from ui import get_user_input, display_results
from ui import generate_date_ranges

# Initialize Chrome Webdriver
driver = webdriver.Chrome()
driver.get("https://vola.ro/")
wait = WebDriverWait(driver, 3)

# Navigation
def allow_cookies(driver):
    try:
        allow_cookies_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, ALLOW_COOKIES_XPATH))
        )
        allow_cookies_element.click()
        print("🙂 Button clicked, cookies allowed 🍪.\n")
        return True
    except Exception:
        print("No button found. Probably cookies have already been accepted.")
        return False

def clear_cache(driver):
    driver.execute_cdp_cmd('Network.clearBrowserCache', {})
    driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
    print("🧹 Cache and cookies cleared.")


def navigate(driver, from_airport, to_airport, departure_date, return_date):
    base_url = (
        "https://www.vola.ro/flight_search/from_code/{}/to_code/{}/dd/{}/rd/{}/ad/1"
    )
    url_to_manipulate = base_url.format(
        from_airport, to_airport, departure_date, return_date
    )
    driver.get(url_to_manipulate)

def get_flight_data(driver):
    # get the price
    # price_xpath = "/html/body/div[1]/div[3]/div/div/div[2]/ith-tab-filters/div/ith-tab-filter[1]/div/strong[1]/span"
    price_xpath = '/html/body/div/div[3]/div/section/div/div[2]/ith-tab-filters/div/ith-tab-filter[1]/div/strong[1]/span'
    price_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, price_xpath))
    )
    time.sleep(10)  # make sure the best price is loaded
    price = price_element.text
    price = re.sub(r'[^\d.]', '', price)  # Remove non-numeric characters

    # get the departure hour
    departure_xpath = "/html/body/div/div[3]/div/section/div/div[2]/ith-flight-offers/div/div[1]/div/div/ith-flight-offer/div/div/div[1]/ith-flight-stage[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/span"
    departure_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, departure_xpath))
    )
    departure_hour = departure_element.text

    # get the return hour
    return_hour_xpath = "/html/body/div/div[3]/div/section/div/div[2]/ith-flight-offers/div/div[1]/div/div/ith-flight-offer/div/div/div[1]/ith-flight-stage[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/span"
    return_hour_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, return_hour_xpath))
    )
    return_hour = return_hour_element.text

    return price, departure_hour, return_hour

def exit_callback(root):
    print("👋 Goodbye! 👋")
    clear_cache(driver)
    driver.quit()
    root.quit()
    root.destroy()
    exit()  # Ensure the entire program stops

def run_logic():
    allow_cookies(driver)
    user_input = get_user_input()
    if user_input:
        from_airport, to_airport, start_date, holiday_duration, search_duration = user_input
        date_ranges = generate_date_ranges(start_date, holiday_duration, search_duration)
        
        best_price = float('inf')
        best_period = None
        best_departure_hour = None
        best_return_hour = None
        best_url = None  # Variable to store the URL of the best price

        print("Generated time slots and associated data:\n")

        for index, (departure_date, return_date) in enumerate(date_ranges, start=1):
            navigate(driver, from_airport, to_airport, departure_date, return_date)
            price, departure_hour, return_hour = get_flight_data(driver)
            price = float(price.replace(',', ''))  # Convert price to float for comparison

            print(f"{index}. ({departure_date}, {return_date})")
            print(f"   Price: {price} EUR 💸")
            print(f"   Departure hour: {departure_hour}")
            print(f"   Return hour: {return_hour}\n")

            if price < best_price:
                best_price = price
                best_period = (departure_date, return_date)
                best_departure_hour = departure_hour
                best_return_hour = return_hour
                best_url = driver.current_url  # Store the current (best) URL

        if best_period:
            departure_date, return_date = best_period
            print("🚀 Program finished, please check your browser.")
            create_db()
            insert_data(
                from_airport,
                to_airport,
                departure_date,
                return_date,
                best_price,
                best_departure_hour,
                best_return_hour,
            )
            display_results(
                from_airport,
                to_airport,
                departure_date,
                return_date,
                best_price,
                best_departure_hour,
                best_return_hour,
                best_url,  # Pass the best URL to display_results
                run_again_callback=run_logic,
                exit_callback=exit_callback,
            )