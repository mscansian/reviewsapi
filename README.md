# Reviews Webservice #
This is just a simple API that allows users to create, list and post reviews

## Setting up ##

### Using docker-compose (recommended) ###
This is the quickest way to get started. Make sure you have Docker and
docker-compose installed in your machine. If you dont, you can follow
[this guide](https://docs.docker.com/install/).

In the project root run the following commands. This will download the correct
Python image from DockerHub, create the environment and start the webservice.

    $ docker-compose up --build

Afterwards use the commands below to migrate the database, create a superuser
and run the test suites. Make sure the docker-compose cmd is still running.

    $ docker exec -it reviewsapi ./manage.py migrate
    $ docker exec -it reviewsapi ./manage.py createsuperuser
    $ docker exec -it reviewsapi ./manage.py test

### Using virtualenv ###
Please, consider using docker. It's easier :)

    $ virtualenv -p python3.6 venv
    $ source venv/bin/activate
    (venv) pip install -r requirements.txt
    (venv) export DJANGO_SECRET_KEY=my-secret-key
    (venv) cd webservice/
    (venv) ./manage.py migrate
    (venv) ./manage.py createsuperuser
    (venv) ./manage.py test
    (venv) ./manage.py runserver 0.0.0.0:8000

Note that by using the virtualenv you are starting the server on port 8000 (not 80).
Remember to change the port on the requests. eg. *http://localhost:8000*.

## Using the API ##

### Authentication ###
The API uses a Token to authenticate users. When you access it for the first time
you need to provide your credentials to fetch the token. On subsequest requests you
can use the token as an HTTP header to authenticate your user agains the service.
Tokens are unique per user and do not expire.

To retrieve your user token you need to make a POST request to *http://localhost/auth/*
with the following json payload

    {
        'username': 'your-username',
        'password': 'password'
    }

If the credentials are correct you will receive a token which you can use to
authenticate the following requests. Send an *Authorization* header with the
work Token followed by your received token.

    Authorization: Token 70c7f0aa64807222a381d7d32eed76d3ede8c38f

### Listing your reviews ###
To list your reviews send a GET request to *http://localhost/reviews/*. Note
that you can only see your own reviews.

### Creating a new review ###
Send a POST request to *http://locahost/reviews/* with the following json payload:

    {
        'company': 'SpaceX',
        'title': "My review",
        'summary': 'This is the best place ever!',
        'rating': 3,
        'author': 'John'
    }

### Retrieving a review ###
Send a GET request to *http://localhost/reviews/<REVIEW-ID>/*. Make sure you replace
*<REVIEW-ID>* with the appropriate id.

### Deleting reviews ###
Reviews are permanent. Where is the fun if you can just delete them? :)

## Convinience settings ##
Some Djago and DRF settings have been enable to facilitate user testing.

### Admin ###
The API has the Django built-in admin configured, you can access it in
*http://localhost/admin/* using superuser credentials to login. The admin
panel allows you to create users, see reviews created by all users and delete reviews.

### BasicAuth ###
It allows you to authenticate using HTTP's username/password basic authentication.
Although is extremelly convinent for testing it's not recommended to use it in
production (especially without TLS). You can disable it by commenting a line in
*webservice/settings.py*.

### DRF Browsable API ###
You can disable the DRF browsable API by commenting a line in *webservice/settings.py*.
