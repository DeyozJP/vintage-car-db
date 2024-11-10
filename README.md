# Vintage Car Database Management

## Overview

This project is a Python-based client-server application that allows users to manage a vintage car database hosted on a Node.js server. It provides a simple command-line interface for users to perform CRUD (Create, Read, Update, Delete) operations on car records. Users can interact with the database to list, add, update, and delete car entries.

## Features

- **List Cars**: View all cars in the database.
- **Add Car**: Add a new car to the database with details such as ID, brand, model, production year, and whether it's convertible.
- **Delete Car**: Delete an existing car from the database by entering its ID.
- **Update Car**: Modify an existing car's details using its ID.

## Requirements

- Python 3.x
- Node.js server hosting a database (e.g., using Express.js and a JSON database)
- `requests` library for Python (for HTTP communication)

## Usage

To run the application, provide the server address, port number (optional), database name (optional), and car ID (optional). 
For example: write in command prompt (python vintage_car_db.py http://localhost)
