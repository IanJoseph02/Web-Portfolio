import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Database setup
def setup_database():
    conn = sqlite3.connect('parking_reservation.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS ParkingReservation (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        LicensePlate TEXT NOT NULL,
                        ReservationStartTime TEXT,
                        ReservationEndTime TEXT,
                        SlotNumber INTEGER,
                        DriverID INTEGER,
                        FOREIGN KEY(DriverID) REFERENCES DriverProfile(ID)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS DriverProfile (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name TEXT,
                        Age INTEGER,
                        Birthdate TEXT,
                        Address TEXT,
                        Email TEXT,
                        Number TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
                        Username TEXT PRIMARY KEY,
                        Password TEXT
                    )''')

    cursor.execute('''INSERT OR IGNORE INTO Admin (Username, Password) 
                      VALUES ('admin', 'admin')''')

    conn.commit()
    conn.close()

# Database operations
def execute_query(query, parameters=(), fetchone=False, commit=False):
    conn = sqlite3.connect('parking_reservation.db')
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchone() if fetchone else cursor.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return result

# Functionality for reservations
def reserve_slot():
    license_plate = entry_license_plate.get()
    selected_driver = listbox_drivers.curselection()
    if not selected_driver:
        messagebox.showerror("Error", "Please select a driver from the list.")
        return

    driver_id = selected_driver[0] + 1
    reservation_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    slot_number = int(entry_slot_number.get())

    execute_query("INSERT INTO ParkingReservation (LicensePlate, ReservationStartTime, SlotNumber, DriverID) VALUES (?, ?, ?, ?)", 
                   (license_plate, reservation_start_time, slot_number, driver_id), commit=True)

    messagebox.showinfo("Info", "Parking Slot Reserved Successfully")
    load_reservation_logs()

def cancel_reservation():
    license_plate = entry_license_plate.get()
    reservation_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    execute_query('''UPDATE ParkingReservation SET ReservationEndTime = ? 
                      WHERE LicensePlate = ? AND ReservationEndTime IS NULL''', 
                   (reservation_end_time, license_plate), commit=True)

    messagebox.showinfo("Info", "Reservation Cancelled Successfully")
    load_reservation_logs()

def reset_reservations():
    execute_query("DELETE FROM ParkingReservation", commit=True)
    messagebox.showinfo("Info", "Reservations have been reset for the new day.")
    load_reservation_logs()

def reset_all_data():
    try:
        execute_query("DELETE FROM ParkingReservation", commit=True)
        execute_query("DELETE FROM DriverProfile", commit=True)
        execute_query("DELETE FROM Admin WHERE Username != 'admin'", commit=True)
        messagebox.showinfo("Info", "All data has been reset.")
        load_driver_profiles()
        load_reservation_logs()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while resetting data: {e}")

# GUI setup
def load_reservation_logs():
    rows = execute_query("SELECT LicensePlate, SlotNumber, ReservationStartTime, ReservationEndTime FROM ParkingReservation")
    listbox_reservations.delete(0, tk.END)
    for row in rows:
        license_plate, slot_number, start_time, end_time = row
        display_text = f"License Plate: {license_plate}, Slot Number: {slot_number}, Start Time: {start_time}, End Time: {end_time if end_time else 'Active'}"
        listbox_reservations.insert(tk.END, display_text)

def load_driver_profiles():
    listbox_drivers.delete(0, tk.END)
    driver_profiles = execute_query("SELECT Name FROM DriverProfile")
    for driver in driver_profiles:
        driver_name = driver[0]
        listbox_drivers.insert(tk.END, driver_name)

def add_driver():
    name = entry_name.get()
    age = entry_age.get()
    birthdate = entry_birthdate.get()
    address = entry_address.get()
    email = entry_email.get()
    number = entry_number.get()

    execute_query("INSERT INTO DriverProfile (Name, Age, Birthdate, Address, Email, Number) VALUES (?, ?, ?, ?, ?, ?)", 
                   (name, age, birthdate, address, email, number), commit=True)

    messagebox.showinfo("Info", "Driver Profile Added Successfully")
    load_driver_profiles()
    reset_driver_form()

def reset_driver_form():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_birthdate.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_number.delete(0, tk.END)

def view_driver_details():
    selected_driver = listbox_drivers.curselection()
    if not selected_driver:
        messagebox.showerror("Error", "Please select a driver from the list.")
        return

    driver_name = listbox_drivers.get(selected_driver[0])
    driver_details = execute_query("SELECT * FROM DriverProfile WHERE Name = ?", (driver_name,), fetchone=True)
    
    if driver_details:
        driver_window = tk.Toplevel(root)
        driver_window.title("Driver Details")

        tk.Label(driver_window, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[1]).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(driver_window, text="Age:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[2]).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(driver_window, text="Birthdate:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[3]).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(driver_window, text="Address:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[4]).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(driver_window, text="Email:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[5]).grid(row=4, column=1, padx=10, pady=5)

        tk.Label(driver_window, text="Phone Number:").grid(row=5, column=0, padx=10, pady=5)
        tk.Label(driver_window, text=driver_details[6]).grid(row=5, column=1, padx=10, pady=5)

        tk.Button(driver_window, text="Close", command=driver_window.destroy).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def check_credentials():
    username = entry_admin_username.get()
    password = entry_admin_password.get()

    result = execute_query("SELECT * FROM Admin WHERE Username = ? AND Password = ?", 
                           (username, password), fetchone=True)
    if result:
        admin_login_window.destroy()
        main_application()
    else:
        messagebox.showerror("Error", "Invalid credentials")

def create_admin_account():
    global create_account_window, entry_new_username, entry_new_password

    create_account_window = tk.Tk()
    create_account_window.title("Create Admin Account")

    tk.Label(create_account_window, text="New Username:").grid(row=0, column=0, padx=10, pady=10)
    entry_new_username = tk.Entry(create_account_window)
    entry_new_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(create_account_window, text="New Password:").grid(row=1, column=0, padx=10, pady=10)
    entry_new_password = tk.Entry(create_account_window, show='*')
    entry_new_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(create_account_window, text="Create Account", command=save_new_admin).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    create_account_window.mainloop()

def save_new_admin():
    username = entry_new_username.get()
    password = entry_new_password.get()

    try:
        execute_query("INSERT INTO Admin (Username, Password) VALUES (?, ?)", (username, password), commit=True)
        messagebox.showinfo("Success", "New admin account created successfully!")
        create_account_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Main application GUI
def main_application():
    global entry_license_plate, entry_slot_number, listbox_reservations, listbox_drivers
    global entry_name, entry_age, entry_birthdate, entry_address, entry_email, entry_number

    global root
    root = tk.Tk()
    root.title("Parking Reservation System")

    # Create GUI widgets and layout
    tk.Label(root, text="License Plate:").grid(row=0, column=0, padx=10, pady=5)
    entry_license_plate = tk.Entry(root)
    entry_license_plate.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Slot Number:").grid(row=1, column=0, padx=10, pady=5)
    entry_slot_number = tk.Entry(root)
    entry_slot_number.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(root, text="Reserve Slot", command=reserve_slot).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(root, text="Cancel Reservation", command=cancel_reservation).grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Reset Reservations", command=reset_reservations).grid(row=2, column=2, padx=10, pady=10)
    tk.Button(root, text="Reset All Data", command=reset_all_data).grid(row=2, column=3, padx=10, pady=10)

    tk.Label(root, text="Reservations:").grid(row=3, column=0, padx=10, pady=5, columnspan=4)
    listbox_reservations = tk.Listbox(root, width=80)
    listbox_reservations.grid(row=4, column=0, columnspan=4, padx=10, pady=5)
    load_reservation_logs()

    tk.Label(root, text="Drivers:").grid(row=5, column=0, padx=10, pady=5, columnspan=4)
    listbox_drivers = tk.Listbox(root, width=80)
    listbox_drivers.grid(row=6, column=0, columnspan=4, padx=10, pady=5)
    load_driver_profiles()

    tk.Label(root, text="Name:").grid(row=7, column=0, padx=10, pady=5)
    entry_name = tk.Entry(root)
    entry_name.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(root, text="Age:").grid(row=8, column=0, padx=10, pady=5)
    entry_age = tk.Entry(root)
    entry_age.grid(row=8, column=1, padx=10, pady=5)

    tk.Label(root, text="Birthdate:").grid(row=9, column=0, padx=10, pady=5)
    entry_birthdate = tk.Entry(root)
    entry_birthdate.grid(row=9, column=1, padx=10, pady=5)

    tk.Label(root, text="Address:").grid(row=10, column=0, padx=10, pady=5)
    entry_address = tk.Entry(root)
    entry_address.grid(row=10, column=1, padx=10, pady=5)

    tk.Label(root, text="Email:").grid(row=11, column=0, padx=10, pady=5)
    entry_email = tk.Entry(root)
    entry_email.grid(row=11, column=1, padx=10, pady=5)

    tk.Label(root, text="Phone Number:").grid(row=12, column=0, padx=10, pady=5)
    entry_number = tk.Entry(root)
    entry_number.grid(row=12, column=1, padx=10, pady=5)

    tk.Button(root, text="Add Driver", command=add_driver).grid(row=13, column=0, columnspan=2, padx=10, pady=10)
    tk.Button(root, text="View Driver Details", command=view_driver_details).grid(row=13, column=2, columnspan=2, padx=10, pady=10)

    root.mainloop()

# Admin login GUI
def admin_login():
    global admin_login_window, entry_admin_username, entry_admin_password

    admin_login_window = tk.Tk()
    admin_login_window.title("Admin Login")

    tk.Label(admin_login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    entry_admin_username = tk.Entry(admin_login_window)
    entry_admin_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(admin_login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    entry_admin_password = tk.Entry(admin_login_window, show='*')
    entry_admin_password.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(admin_login_window, text="Login", command=check_credentials).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    tk.Button(admin_login_window, text="Create Admin Account", command=create_admin_account).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    admin_login_window.mainloop()

setup_database()
admin_login()
