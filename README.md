# Car Registry App

This is a simple car registry app written in Python using the Streamlit library for creating the UI and SQLite for database management.

## Features

- **Add a new car and driver to the database.**
- **View all drivers and their associated cars.**
- **Delete a driver and their associated car from the database.**
- **Update car and driver details in the database.**

## Requirements

Python 3.6+
Streamlit
SQLite

You can install the required libraries using pip:
pip install streamlit sqlite3


## Code Overview

The code is divided into several sections:

Database connection and table creation: Here we establish a connection to a SQLite database 'cars.db'. If the database doesn't exist, it's created. The tables cars and drivers are also created if they don't exist.

Data for the Streamlit UI: Lists of car models, years, driver names, surnames, and car registrations are created. These will be used in the Streamlit UI for selection.

Function definitions: The functions add_car, delete_driver, view_drivers, and get_car are defined. These functions handle the interaction with the SQLite database, inserting, deleting, viewing, and updating data as necessary.

Streamlit app: In the main function, the Streamlit UI is defined. Depending on the user's selection in the sidebar, different sections of the UI are displayed and the corresponding database function is called.

## How to Run

To run the application, navigate to the directory containing the script and use the following command:
streamlit run <script_name.py>


Replace `<script_name.py>` with the name of the Python script.

Once the application is running, navigate to http://localhost:8501 in your web browser to view the app.

## Usage

In the sidebar of the app, you'll find four options:

Add a new car and driver: This will show you a form to input the details of the car and driver. Fill in the information and click "Add". The new car and driver will be added to the database.

View all drivers and their cars: This will display a dropdown with the names of all drivers in the database. Selecting a driver will display their details, as well as the details of their car.

Delete a driver and their car: This will show you an input field to enter the ID of the driver you wish to delete. Click "Delete" to remove the driver and their car from the database.

Update a car and driver: This will show you an input field to enter the ID of the car you wish to update. Enter the ID and click "Update". You'll then see the current details of the car and driver, and you can input new information to update these details.



