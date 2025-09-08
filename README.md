# Full Stack Application Development Capstone Project

This repository has the project code for the Full Stack Application Development Capstone Project. Part of IBM Full Stack Software Developer Professional Certificate on Coursera.

---

## Project Details

---

### Project Title: Car Dealership Review Portal

You will assume the role of a Full Stack Developer hired by Best Car Dealership, a national car dealership with branches all over the US. You will create a website that provides a central database of dealership reviews across the country.

You will be provided with a project scenario that requires you to develop the website and the required backend services.

---

## Building MongoDB Database

### Building Express Server

Using docker to build the server
First go to the database folder

```sh
cd server/database
docker build . -t nodeapp
```

Then run compose to run the server and mongo db

```sh
docker-compose up
```

## Adding Models to SQLite Database from Django

First create `CarMake` and `CarModel` models in `server/djangoapp/models.py`

Then register the models in `server/djangoapp/admin.py`

Then run the following commands to create migrations and migrate the database

```sh
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

## Setting Express MongoDB Backend in Django (Building Proxy to Express Server)

In `.env` file add the following line

```env
backend_url=http://<your-express-server-url>/
```

## Deploying Sentiment Analyzer Microservice

### 1. Change to the sentiment_analysis folder

```sh
cd server/djangoapp/microservices
```

### 2. Build sentiment analyzer docker image

```sh
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### 3. Push the image to IBM Cloud Container Registry

```sh
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
```

### 4. Deploy the sent_analyzer application on code engine

```sh
ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000
```
