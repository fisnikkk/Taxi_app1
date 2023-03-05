import streamlit as st
import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('cars.db')
c = conn.cursor()

#Tabela1
c.execute('''CREATE TABLE IF NOT EXISTS cars
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             model TEXT,
             year INTEGER,
             registration TEXT,
             driver_id INTEGER,
             FOREIGN KEY(driver_id) REFERENCES drivers(id))''')

#Tabela2
c.execute('''CREATE TABLE IF NOT EXISTS drivers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             surname TEXT,
             phone INTEGER,
             birthday TEXT)''')

car_models = ['Mercedes', 'BMW', 'Toyota', 'Honda'] # list of car models to choose from
years = [year for year in range(1900, datetime.now().year+1)] # list of years to choose from
names = ['John', 'Jane', 'Bob', 'Alice'] # list of names to choose from
surnames = ['Smith', 'Doe', 'Johnson', 'Williams'] # list of surnames to choose from
registrations = ['ABC123', 'DEF456', 'GHI789', 'JKL012'] # list of car registrations to choose from

# Funksion me shtu vozites dhe shofer
def add_car(model, year, registration, name, surname, phone, birthday):
    # Insert driver into drivers table
    c.execute("INSERT INTO drivers (name, surname, phone, birthday) VALUES (?, ?, ?, ?)", (name, surname, phone, birthday))
    driver_id = c.lastrowid # Get the last inserted id
    
    # Insert car into cars table with the driver's id
    c.execute("INSERT INTO cars (model, year, registration, driver_id) VALUES (?, ?, ?, ?)", (model, year, registration, driver_id))
    conn.commit()

# Funksion me i fshi
def delete_driver(driver_id):
    # Delete the driver and their car from the database
    c.execute("DELETE FROM cars WHERE driver_id=?", (driver_id,))
    c.execute("DELETE FROM drivers WHERE id=?", (driver_id,))
    conn.commit()

# Funksioni me i pa krejt voizitsat
def view_drivers():
    # Join cars and drivers tables on driver_id
    c.execute("SELECT cars.registration, cars.model, cars.year, drivers.name, drivers.surname, drivers.phone, drivers.birthday FROM cars INNER JOIN drivers ON cars.driver_id = drivers.id")
    drivers = c.fetchall()
    driver_names = [f"{driver[3]} {driver[4]}" for driver in drivers]
    selected_driver = st.selectbox("Select a driver", driver_names)
    index = driver_names.index(selected_driver)
    selected_driver_details = drivers[index]
    st.write(f"Registration: {selected_driver_details[0]}, Model: {selected_driver_details[1]}, Year: {selected_driver_details[2]}, Driver Name: {selected_driver_details[3]} {selected_driver_details[4]}, Phone: {selected_driver_details[5]}, Birthday: {selected_driver_details[6]}")


def get_car(car_id, model=None, year=None, name=None, surname=None, car_registration=None, driver_id=None):
    if model is not None and year is not None:
        c.execute("UPDATE cars SET model=?, year=? WHERE id=?", (model, year, car_id))
    if name is not None and surname is not None:
        c.execute("UPDATE drivers SET name=?, surname=? WHERE id=(SELECT driver_id FROM cars WHERE id=?)", (name, surname, car_id))
    if car_registration is not None:
        c.execute("UPDATE cars SET registration=? WHERE id=?", (car_registration, car_id))
    if driver_id is not None:
        c.execute("UPDATE cars SET driver_id=? WHERE id=?", (driver_id, car_id))
    conn.commit()
    c.execute("SELECT cars.id, cars.model, cars.year, cars.registration, drivers.name, drivers.surname FROM cars JOIN drivers ON cars.driver_id=drivers.id WHERE cars.id=?", (car_id,))
    car = c.fetchone()
    return car

# Streamlit app
def main():
    st.title("Car Registry")

    menu = ["Add a new car and driver","View all drivers and their cars", "Delete a driver and their car", "Update a car and driver"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Shto nje veture dhe shofer
    if choice == "Add a new car and driver":
        st.subheader("Shto nje vetur dhe nje vozites")
        model = st.selectbox("Modeli i vetures", car_models)
        year = st.slider("Viti i prodhimit(jo me te vjeter se 2015)", min_value=2015, max_value=2023)
        registration = st.selectbox("Cakto regjistrimin e vetures",registrations)
        name = st.selectbox("Cakto emrin vozitesit",names)
        surname = st.selectbox("Cakto mbiemrin vozitesit",surnames)
        phone = st.text_input("Shkruaj numrin e telefonit")
        birthday = st.date_input("Vendos datelindjen(jo nen 18vjec)",
                         min_value=datetime(1960, 1, 1),
                         max_value=datetime(2004, 12, 31),
                         value=datetime(1990, 1, 1),
                         )

        if st.button("Add"):
            add_car(model, year, registration, name, surname, phone, birthday)
            st.success("Car and driver added to the database!")





    # Shfaq te gjithe vozitesit me veturat e tyre
    elif choice == "View all drivers and their cars":
        st.subheader("Shfaq te gjithe vozitesit me veturat e tyre")
        view_drivers()

    

    # Fshi nji vozites
    elif choice == "Delete a driver and their car":
        st.subheader("Delete a driver and their car")
        driver_id = st.text_input("Enter driver id")
    
        if st.button("Delete"):
            delete_driver(driver_id)
            st.success("Driver and their car deleted from the database!")

    #Perditso te dhenat
    elif choice == "Update a car and driver":
        st.subheader("Update a car and driver")
        car_id = st.text_input("Enter car id")
        car = get_car(car_id)

        if car:
            st.write(f"Registration: {car[3]}, Model: {car[1]}, Year: {car[2]}")
            new_model = st.selectbox("Enter new car model", car_models, index=car_models.index(car[1]))
            new_year = st.selectbox("Enter new car year", years, index=years.index(car[2]))
            new_name = st.text_input("Enter new driver name", value=car[4])
            new_surname = st.text_input("Enter new driver surname", value=car[5])

            if st.button("Update"):
                get_car(car_id, new_model, new_year, new_name, new_surname)
                st.success("Car and driver updated in the database!")
        else:
            st.warning("Car id not found in the database")

if __name__ == '__main__':
    main()