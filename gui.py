import PySimpleGUI as sg
from datetime import datetime

# Importing from other files
from xpaths import YEAR


def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_user_input():
    layout = [
        [
            sg.Text("Enter the 3-letter airport code you're flying from, ex BUH:"),
            sg.InputText(key="from_airport"),
        ],
        [
            sg.Text("Enter the 3-letter airport code you're flying to:"),
            sg.InputText(key="to_airport"),
        ],
        [
            sg.Text("Enter departure month and day (MM-DD):"),
            sg.InputText(key="departure_month_day"),
        ],
        [
            sg.Text("Enter return month and day (MM-DD):"),
            sg.InputText(key="return_month_day"),
        ],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("Flight Search", layout)
    event, values = window.read()
    window.close()

    if event == "Cancel" or event is None:
        return None

    from_airport = values["from_airport"].upper()
    to_airport = values["to_airport"].upper()
    departure_month_day = values["departure_month_day"]
    return_month_day = values["return_month_day"]

    if len(from_airport) != 3 or not from_airport.isalpha():
        sg.popup("Invalid departure airport code format. Please try again.")
        return get_user_input()
    if len(to_airport) != 3 or not to_airport.isalpha():
        sg.popup("Invalid arrival airport code format. Please try again.")
        return get_user_input()
    if not validate_date(f"{YEAR}-{departure_month_day}"):
        sg.popup("Invalid departure date format. Please try again.")
        return get_user_input()
    if not validate_date(f"{YEAR}-{return_month_day}"):
        sg.popup("Invalid return date format. Please try again.")
        return get_user_input()

    departure_date = f"{YEAR}-{departure_month_day}"
    return_date = f"{YEAR}-{return_month_day}"

    return from_airport, to_airport, departure_date, return_date


def display_results(
    from_airport,
    to_airport,
    departure_date,
    return_date,
    price,
    departure_hour,
    return_hour,
):
    layout = [
        [sg.Text(f"From: {from_airport}")],
        [sg.Text(f"To: {to_airport}")],
        [sg.Text(f"Departure Date: {departure_date}")],
        [sg.Text(f"Return Date: {return_date}")],
        [sg.Text(f"Price: {price} RON")],
        [sg.Text(f"Departure Hour: {departure_hour}")],
        [sg.Text(f"Return Hour: {return_hour}")],
        [sg.Button("Run Again"), sg.Button("Exit")],
    ]

    window = sg.Window("Flight Results", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Run Again":
            window.close()
            return True
    window.close()
    return False
