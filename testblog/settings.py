"""
Django settings for testblog project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from os import getenv
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_7kifta98%yi@6a=#97&423-lw9)*-mhv&gm3l#-=k%s+3skiu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # we set to false after finishing development period
# getenv("developing",True)
ALLOWED_HOSTS = [ ] # we set the default to be localhost so it will be using the local host during the developing phase and the hots name during deploying
#[ getenv("allowed_hosts", "localhost")]

# Application definition

INSTALLED_APPS = [
    'blog',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'testblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "challenges" / "templates",
            BASE_DIR / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'testblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres', # postgres is the default name if nothing was choosen
        'USER': 'test' , # this is Master username we find this data in configuration
        'PASSWORD': 'Safya1990' ,
        'HOST': 'database-2.c960k4aeucjl.eu-north-1.rds.amazonaws.com', # this is the end point and we get it from connectivity and security
        'PORT': '5432'
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#STATIC_ROOT = BASE_DIR / "static_files" # wee need to create this before deployment to collect all static files in one folder
# then we need to run python3 manage.py collectstatic
# if we made in change in any static file we need to run python3 manage.py collectstatic again



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / "uploads" # we need to add this folder in settings before we use it as a folder for users to upload to
MEDIA_URL = "/files/" # we need to creat this url so django use it as url for files uploaded by users or files in general which we acces with iamge.url

"""
changes we made in settings.py 
we add any new app we create in INSTALLED_APPS

we add this :
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
so django will use static folder in main project folder

MEDIA_ROOT = BASE_DIR / "uploads" # we need to add this folder in settings before we use it as a folder for users to upload to
MEDIA_URL = "/files/" # we need to creat this url so django use it as url for files uploaded by users or files in general which we acces with iamge.url

before deployment:

we need to set debug to false

STATIC_ROOT = BASE_DIR / "static_files" # wee need to create this before deployment to collect all static files in one folder
STATIC_URL = '/static/' # django will use this url so to connect with static files
# then we need to run python3 manage.py collectstatic
# if we made in change in any static file we need to run python3 manage.py collectstatic again
then we need to go to urls.py in main project and add

from django.conf import settings
from django.conf.urls.static import static

+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
we add it at the end of the urlpatterns 
we only add  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  in case we are working with small websites and wants django to handle the static files
then we should run migrations again just in case 
and we should make sure we created the superuser
python3 manage.py createsuperuser

then we need to run
python3 -m pip freeze > requiremnets.txt 
this will create a file that lock all the packages we installed in our system in this case django package and extra packages in this case pillow package since we are using imagefield
but this will create a long list with packages that might not be necessary so better to create a virtual environment using this command in the VSCode terminal
python3 -m venv any_name_of_choice in case we did not start virtual environment at the beginning of the project
then we install the packages we used
python3 -m pip install Django pillow # we can add any more packages
then run 
python3 -m pip freeze > requiremnets.txt 

then we need to add the allowed hosts and for this we need to:
from os import getenv

then allowed hosts we can use getenv("anyname")
we can do that also in SECRET_KEY

SECRET_KEY = getenv("anything") to hide it from github

DEBUG = getenv("developing",True)

allowed_hosts   getenv('the value', 'localhost') # we set the default to be localhost so it will be using the local host during the developing phase and the hots name during deploying



"""

"""
if we want to connect psotgre sql 
we go to postgresql django then install the package 

pip install django psycopg2-binary
then we need to run 
python3 -m pip freeze > requiremnets.txt

now we need to have a data base which could be for money or a free one in aws
we look for RDS which is a managed one so a lot will be taken care of
and then we choose databases
choose postgre and in templates choose free tier
mose of options keep default we make public access yes so we can access the database outside the django app
IMPORTANT very important create a security group 
IMPORTANT after data base is created we have to go o the security group and change the inbound Rule to choose the option any 0.0.0.0 so everyone can access it from anywhere
look at more options
usually we should use two data bases one for while developing and one after developing for the actuall use
then n settings.py we go to 
DATABASES
and change it to 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djano', # this the DB name in configuration
        'USER': 'django' , # this is Master username we find this data in configuration
        'PASSWORD': 'Yasser1990' ,
        'HOST': 'database-1.c960k4aeucjl.eu-north-1.rds.amazonaws.com', # this is the end point and we get it from connectivity and security
        'PORT': '5432'
    }
    }
    we can use getenv() for this data to protect it

    then we run migrations

    then we can go to admin page of our webste and use the username and passwprd we used to create the database

"""

"""
deploying via render
VIRTUAL ENV anything in virtual env

first  to handle static
pip install whitenoise

Then ADD to 
MIDDLEWARE:
'whitenoise.middleware.WhiteNoiseMiddleware',
after the first line
then after the stati root we add this line

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
then 

pip install gunicorn

render only supoorts django 3.2 or less
so
pip install django==3.2.1
then create a in the main project directory a file called build.sh
this file is the same for all platforms and has the same three commands
then run 
install necessary installs like
pip install psycopg2-binary
python3 -m pip install Django pillow
then run
python3 -m pip freeze > requiremnets.txt
then we need to push to git hub
then gi to render dashboard
then change 
Build Command sh bulid.sh
Start Command  gunicorn testblog.wsgi # the name of the folder containg wsgi

"""