# TechnicalChallenge

Clever Advertising Technical Challenge

This challenge consisted on the implementation of a Script to retrieve the GINI index in brasil for the year of 1991. Furthermore, A FastAPI application was developed using the Script to access, delete and update data. Upon initialization of the FastAPI, the Script will scrape automatically so it might take a while for the application to fully load.
Individual usage of the script can be achieved by altering the relative imports in the `/src` files.

#### Overview

The scraper is composed by the Scraper, FileFinder, and Processor classes, at `app/src/services`:

1. **Scraper** (scraper.py): Uses `BeautifulSoup4` and the `requests `library to access the FTP server and download all the GINI91 ZIP Files to the `/Archives` Folder
2. **Processor** (data_processor.py): Uses the `zip` library to extract the files from the `/Archives` folder and then uses the `pandas` library to read the remaining `.XLS` files and generates a `LocationData` model from the processed data
3. **FileFinder** (file_finder.py): Provides Static Methods to Cleanup And Find Files of a specified type in a specified folder

Furthermore, the **Repository** class at `app/src` provides  methods to connect to the database and to insert, update, delete, retrieve and filter all the processed data from the database.

The `models.py` script contains the implementation of the `LocationData` data structure:

* **Attributes**
  * **location** (`str`): Represents the name of the location.
  * **region** (`str`): Represents the name of the region associated with the location.
  * **region_code** (`str`): Represents a code that abreviates the region (follows the location in the data source).
  * **value** (`float`): Represents a numerical value associated with the location, such as a metric or statistic.

## Usage

This is a guide on how to use only the scraper that downloads ZIP files from an FTP server, extracts the contents, processes Excel files, and saves relevant data to a database.

### Configurations

The `configs.json` file provides a method of easily changing the application settings.

#### Explanation of Fields:

* **`folder`** : The directory where scraped data and downloaded files will be stored. If the folder doesn't exist, the application will attempt to create it.
* **`url`** : The target URL from where the scraper fetches the `.zip` files.
* **`country`** : Specifies the country or region being targeted in the data processing (in this case, "Brasil").
* **`configuration`** :
  * **`host`** : The hostname for the database server (`localhost` if FastAPI not using docker, else it is the container name).
  * **`user`** : The database username that has access to the target database.
  * **`password`** : The password for the specified database user.
  * **`database`** : The name of the database where processed data will be stored.
  * **`table_name`** : The specific table within the database where location data will be inserted.

Default Values:

```
{
    "folder": "Archives",
    "url": "https://ftp.ibge.gov.br/Censos/Censo_Demografico_1991/Indice_de_Gini/",
    "country": "Brasil",
    "configuration": {
        "host": "localhost",
        "user": "user",
        "password": "root",
        "database": "technicalchallenge",
        "table_name": "locationData"
    }
}

```

### Using the Scraper and FastAPI Locally

To run the FastAPI locally, you need to:

* Clone the Repository
* Change Configs.json property `configuration.host` value to `'localhost'`. This points the FastAPI Application to the Database Container
* Open CMD and Run this to Create the mySQL Container:

  ```
  docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=technicalchallenge -e MYSQL_USER=user -e MYSQL_PASSWORD=root -p 3306:3306 --restart always mysql
  ```

  * To Access the mysql server in the docker container run: `docker exec -it mysql mysql -u user -p`
* Inside the TechnicalChallenge folder run:

  * Create a new Virtual Environment:

    ```
      python -m venv env
    ```
  * Activate the environment

    ```
    .\env\Scripts\activate
    ```
  * Install the Requirements

    ```
    pip install -r requirements.txt
    ```
  * Run the FastAPI Application Script:

    ```
    uvicorn app.main:app --reload
    ```
  * Refer to `localhost:8000/docs` to access the Swagger Documentation

The scraper will now initialize and run until it saves all the data to the database. Any error will be printed in the terminal

### Using Docker

* Clone the Repository
* Change Configs.json property `configuration.host` value to `'mysql'`. This points the FastAPI Docker Container to the Database Container
* Open CMD and Run:
  ```
  docker-compose up
  ```
* Two containers will now be created, the FastAPI container and the mySQL Database. The Application should be deployed at [localhost:8000](http://localhost:8000)
* Refer to `localhost:8000/docs` to access the Swagger Documentation

# FAST API

The FastAPI application was developed using the previously defined scraper to add more CRUD functionalities to the project

## 1. Run the Scraper

- **Endpoint**: `GET /scrape`
- **Description**: Triggers the scraper to run and download data from the external source.
- **Response**:
  - **Success**:
    ```json
    {
      "status": "success"
    }
    ```
  - **Error**:
    ```json
    {
      "status": "error",
      "message": "<error_message>"
    }
    ```

## 2. Search for Items

- **Endpoint**: `GET /`
- **Parameters**:
  - `location` (Optional): The location (city name).
  - `region` (Optional): The region (region name).
- **Description**: Retrieves items from the database based on the provided location and/or region.

## 3. Delete Items

- **Endpoint**: `DELETE /`
- **Parameters**:
  - `location` (Optional): The location (city name).
  - `region` (Optional): The region (region name).
- **Description**: Deletes items matching the specified location and region.

## 4. Update Item

- **Endpoint**: `PUT /{region}/{location}`
- **Parameters**:
  - `region`: The region of the item to update.
  - `location`: The location of the item to update.
  - `item_data`: JSON body containing updated item data (must conform to `LocationDataResponse`).
- **Description**: Updates the specified item in the database.
