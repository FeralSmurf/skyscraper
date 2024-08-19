# logic.py
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time

# Importing from other files
from db import create_db, insert_data
from xpaths import ALLOW_COOKIES_XPATH, YEAR
from ui import get_user_input, display_results

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
    price_xpath = "/html/body/div[1]/div[3]/div/div/div[2]/ith-tab-filters/div/ith-tab-filter[1]/div/strong[1]/span"
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, price_xpath))
    )
    time.sleep(10)  # make sure the best price is loaded
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


def exit_callback(root):
    print("👋 Goodbye! 👋")
    driver.quit()
    root.quit()
    root.destroy()
    exit()  # Ensure the entire program stops


def run_logic():
    allow_cookies(driver)
    user_input = get_user_input()
    if user_input:
        from_airport, to_airport, departure_date, return_date = user_input
        navigate(driver, from_airport, to_airport, departure_date, return_date)
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
        display_results(
            from_airport,
            to_airport,
            departure_date,
            return_date,
            price,
            departure_hour,
            return_hour,
            run_again_callback=run_logic,
            exit_callback=exit_callback,
        )
