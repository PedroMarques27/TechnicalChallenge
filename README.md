# TechnicalChallenge

Clever Advertising Technical Challenge

## Local Setup

For local setup, create a virtual environment:

```
  python -m venv env

```

To active the virtual environment use:

```
  .\env\Scripts\activate 

```

Download Requirements using the following command:

```
  pip install -r requirements.txt
```

## FastAPI: Installation and Initialization

**To Initialize the system just run the following:**

```
  docker-compose up -- build

```

**To Access the Database Run**

```
docker exec -it mysql mysql -u user -p
```

Afterwards just enter the username and the password configured in the docker-compose.yml file. 
Default is root:root
