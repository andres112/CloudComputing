# WATCHES
## WEB SERVICES
### PART 1
### Deliverables
This project contains the following cmponents:
* **server.py** The web service code in python
* **run.sh** Script to run the web service 
* **requirements.txt** Contains the modules to execute the web serivice
* **Dockerfile** Contains the configuration to mount the web service in a Docker container
* **docker-compose.yml** Contains the configuration of the services to compose them as one on Docker
* **/db** Folder that contains the **watches.sql** database to be mounted in the mysql service on Docker

### Features and objectives reached
The web service has the following routes, where through HTTP request the service response:
* **POST** /watch 
* **GET** /watch/{sku}
* **PUT** /watch/{sku}
* **DELETE** /watch/{sku}
* **GET** /watch/complete-sku/{prefix}
* **GET** /watch/find?"query_strings"

* The data persistence is possible to **MySql** RMDB
* The user authentication is possible with **HTTP Basic Auth**
* The optional goal about the DataBase indexis was successful implemented
* All the ENV variables were created and configurated.
* The service composed contains the following images: MySQL image version 5.7, PHPMyAdmin and the watches web service
* The optional goal about the HTTP expiration data is pending

### Test
Before to the Docker part, the web service was tested in the in the swagger environment, this test was possible thanks to the _info_openapi_v1.yaml_ given by the Lecture professor. The test got successful result.

[Test Link](https://editor.swagger.io/) (It is required to import the _info_openapi_v1.yaml_ file)