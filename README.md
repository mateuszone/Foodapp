## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This is a simple app on which you can plan your meals, orginally developed in Polish Language. You can store your recipies
and meal plans, and add new whenever you need to update ;)
	
## Technologies
Project is created with:
* Python 3.7
* Django 3.2
* HTML 5
* CSS
* Javascript 6

## Setup
First you should clone this repository:

```
$ git clone https://github.com/mateuszone/Foodapp.git
$ cd  Foodapp
```
To run the project you should have Python 3 installed on your computer. Then it's recommended to create a virtual environment for your projects dependencies. To install virtual environment:

pip install virtualenv

Then run the following command in the project directory:

virtualenv venv

That will create a new folder venv in your project directory. Next activate virtual environment:

```
$ source venv/bin/active
```

Then install the project dependencies:

```
$ pip install -r requirements.txt
```

In scrumlab directory create local_settings.py, you can use code below or configure different db_system

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}
```

Now you have to makemigrations and then migrate:

```
$ python manage.py makemigrations
$ python manage.py migrate

```


Create superuser:

```
$ python manage.py createsuperuser
```

Now you can run the project with this command:

```
$ python manage.py runserver
```

## Note
in the settings file you should complete your own database settings.</br>
To makeapp fully working add some records from /admin site or shell because some views need last_created_record so there is need to have at least one to make that app fully functional.








