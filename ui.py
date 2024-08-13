import tkinter as tk
from tkinter import messagebox, ttk
from utils import validate_date
from xpaths import YEAR

# List of European airport codes with corresponding cities
from xpaths import AIRPORT_CODES


# Create a list of options for the dropdown menu
DROPDOWN_OPTIONS = [f"{code} - {city}" for code, city in AIRPORT_CODES.items()]


def custom_input_dialog(title, prompt, initialvalue="", options=None):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("800x600")

    large_font = ("FiraCode", 14)

    tk.Label(dialog, text=prompt, font=large_font).pack(pady=20)

    if options:
        combo = ttk.Combobox(dialog, values=options, font=large_font)
        combo.pack(pady=20)
        combo.set(initialvalue)  # Set the initial value
    else:
        entry = tk.Entry(dialog, font=large_font)
        entry.pack(pady=20)
        entry.insert(0, initialvalue)  # Insert the initial value

    result = []

    def on_ok(event=None):
        if options:
            selected_option = combo.get()
            result.append(selected_option.split(" - ")[0])  # Extract the airport code
        else:
            result.append(entry.get())
        dialog.destroy()

    tk.Button(dialog, text="OK", command=on_ok, font=large_font).pack(pady=20)
    dialog.bind("<Return>", on_ok) # Bind Enter key to the on_ok function
    dialog.bind("<KP_Enter>", on_ok) # Bind NumPad Enter key to the on_ok function 
    if options:
        combo.focus_set()  # Set focus to the combo widget
    else:
        entry.focus_set()  # Set focus to the entry widget

    dialog.transient()
    dialog.grab_set()
    dialog.wait_window()

    return result[0] if result else None


def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    from_airport = custom_input_dialog(
        "Input",
        "Enter the 3-letter airport code you're flying from, ex BUH:",
        "BUH",
        DROPDOWN_OPTIONS,
    )
    if not from_airport:
        return None
    from_airport = from_airport.upper()

    to_airport = custom_input_dialog(
        "Input",
        "Enter the 3-letter airport code you're flying to:",
        "",
        DROPDOWN_OPTIONS,
    )
    if not to_airport:
        return None
    to_airport = to_airport.upper()

    departure_month_day = custom_input_dialog(
        "Input", "Enter departure month and day (MM-DD or MM.DD or MM DD):"
    )
    if not departure_month_day:
        return None

    return_month_day = custom_input_dialog(
        "Input", "Enter return month and day (MM-DD or MM.DD or MM DD):"
    )
    if not return_month_day:
        return None

    if len(from_airport) != 3 or not from_airport.isalpha():
        messagebox.showerror(
            "Error", "Invalid departure airport code format. Please try again."
        )
        return get_user_input()
    if len(to_airport) != 3 or not to_airport.isalpha():
        messagebox.showerror(
            "Error", "Invalid arrival airport code format. Please try again."
        )
        return get_user_input()

    while True:
        if not validate_date(departure_month_day):
            messagebox.showerror(
                "Error", "Invalid departure date format. Please try again."
            )
            departure_month_day = custom_input_dialog(
                "Input", "Enter departure month and day (MM-DD or MM.DD or MM DD):"
            )
            if not departure_month_day:
                return None
            continue

        if not validate_date(return_month_day):
            messagebox.showerror(
                "Error", "Invalid return date format. Please try again."
            )
            return_month_day = custom_input_dialog(
                "Input", "Enter return month and day (MM-DD or MM.DD or MM DD):"
            )
            if not return_month_day:
                return None
            continue

        break

    departure_date = f"{YEAR}-{departure_month_day.replace('.', '-').replace(' ', '-').replace('/', '-')}"
    return_date = f"{YEAR}-{return_month_day.replace('.', '-')}"

    return from_airport, to_airport, departure_date, return_date


def display_results(
    from_airport,
    to_airport,
    departure_date,
    return_date,
    price,
    departure_hour,
    return_hour,
    run_again_callback,
    exit_callback,
):
    root = tk.Tk()
    root.title("Flight Results")

    # Define a larger font
    large_font = ("FiraCode", 14)

    # Set the window size to be larger
    root.geometry("800x600")

    tk.Label(
        root,
        text=f"From: {from_airport} ({AIRPORT_CODES.get(from_airport, 'Unknown')})",
        font=large_font,
    ).pack(pady=20)
    tk.Label(
        root,
        text=f"To: {to_airport} ({AIRPORT_CODES.get(to_airport, 'Unknown')})",
        font=large_font,
    ).pack(pady=20)
    tk.Label(root, text=f"Departure Date: {departure_date}", font=large_font).pack(
        pady=20
    )
    tk.Label(root, text=f"Return Date: {return_date}", font=large_font).pack(pady=20)
    tk.Label(root, text=f"Price: {price} RON", font=large_font).pack(pady=20)
    tk.Label(root, text=f"Departure Hour: {departure_hour}", font=large_font).pack(
        pady=20
    )
    tk.Label(root, text=f"Return Hour: {return_hour}", font=large_font).pack(pady=20)
    tk.Button(root, text="Run Again", command=run_again_callback, font=large_font).pack(
        pady=20
    )
    tk.Button(
        root, text="Exit", command=lambda: exit_callback(root), font=large_font
    ).pack(pady=20)
    root.mainloop()


def exit_callback(root):
    root.quit()
    root.destroy()
    exit()  # Ensure the entire program stops

