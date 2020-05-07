# Cura Network Interview App

This is a Django app that uses
[Here Places](https://www.here.com/) to get property informations i.e hotels

##### This app is written with Django 3.0.5.

You can view a working version of this app
[here](https://curanetwork.herokuapp.com/).

Running this app on your local machine in development will work as
well

## Building

It is best to use the python `virtualenv` tool to run locally:

```sh
$ git clone https://github.com/rammyblog/cura_network.git
$ cd cd cura_network
$ virtualenv-3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

There are some Environment variables that the app is dependent on

To create the .env file cd into cura_network folder

```sh
$ cd cd cura_network
$ ls
__init__.py settings.py urls.py wsgi.py
$ touch .env
```

In the .env file paste the following

```
DEBUG=on
SECRET_KEY=39wkevnve%@kf4q%36!aeg4*e855zso2e1qp_ho17@ey5x^i2!
HERE_API_KEY=Your Here Api Key
HERE_APP_ID= Your Here App Id
```

The App uses your Local Postgres DB by default, all you have to do is create a new
database in your pgAdmin named `cura_network`.

Or you can use the default Django Sqlite using the following settings
in your settings.py

```

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

or you can use your postgres details as well.

```
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': ‘<db_name>’,

        'USER': '<db_username>',

        'PASSWORD': '<password>',

        'HOST': '<db_hostname_or_ip>',

        'PORT': '<db_port>',

    }

}

```

After setting up your database and .env file run the following commands

```sh
$ python manage.py migrate
$ python manage.py runserver
```

### [Read The Api Hosted Docs](https://curanetwork.herokuapp.com/docs/)

### [Read The Api Local server Docs](http://127.0.0.1:8000/docs/)

Then visit `http://127.0.0.1:8000` to view the app.

### To run tests

The tests checks for the following

#### Creating a booking and confirms with the db by counting the number of bookings

#### Counting the number of bookings by creating a booking

#### Getting a list of properties in an area using HERE API and confirm whether the output data type gotten corresponds with a default provided

```
    python3 manage.py tests
```
