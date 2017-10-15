# StreetSmartCities-API

This repository contains the endpoints and models used within the backend for StreetSmart Cities. The backend is run using Django and Postgres, and has only RESTful components. The API current supports the following operations:

* `get_city` - Returns a representation of a city given an ID
* `get_user` - Returns a representation of a user
* `generate_tasks` - Generates a list of tasks for debugging and demo purposes
* `get_tasks` - Returns a list of all tasks for the current city
* `delete_tasks` -  Deletes all tasks (debugging purposes)
* `analyze_iot` - See section below for more details
* `get_data` - Returns the data retreived from `analyze-iot`

### GE Current

The `analyze_iot` method does data parsing and mining on the GE Current API, which provides real-time IoT information for cities and enterprises. If you would like to see how this works, takes a look at the Jupyter Notebook `current.ipynb`, which I used to test run my process first. I essentially consolidated, filtered, and cleaned results from the original API into a form that I wished to use.

### Deployment

The Procfile located within the roor directory has all commands needed to run this site, which is essentially a simple Django server.