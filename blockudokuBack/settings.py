import psycopg2
from    django.http                  import HttpResponse
from email.mime.multipart import MIMEMultipart
from   email.mime.text      import MIMEText
from   datetime             import datetime
from   django.urls          import resolve
from   pathlib              import Path
import smtplib
import os
# nemelt importuud 
import hashlib
import base64
import random
from smtplib import SMTPDataError
import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g@-hfrjss64w=jaz!-l9i(r2$9$-nk)_n$hq61$pzoc+$#gk$6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blockudokuBack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'blockudokuBack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#############################
pgDbName   = "blockudoku"
pgUser     = "user"
pgHost     = "192.168.0.235"
pgPassword = "postgres"
pgPort     = "5432"
######################
def mandakhHash(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()
#   mandakhHash

## Бүртгүүлэхэд автоматаар үүсэх 5 оронтой код
def createPassword(length):
    # Random string of length 5
    result_str = ''.join((random.choice('abcdefghjkmnpqrstuvwxyz123456789$!?') for i in range(length)))
    return result_str
    # Output example: ryxay
#   createPassword

## Хэрэглэгчийн бүртгэл баталгаажуулах код үүсгэнэ. 
## 30 тэмдэгт байгаа. 
## length нь үсгийн урт
def createCodes(length):
    # Random string of length 30
    result_str = ''.join((random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length)))
    return result_str
    # Output example: ryxay
#   createCodes


def base64encode(length):
    return base64.b64encode((createCodes(length-26) + str(datetime.now().time())).encode('ascii')).decode('ascii').rstrip('=')

#   base64encode

def get_view_name_by_path(path):
    result = resolve(path=path)
    return result.view_name
#   get_view_name_by_path

def pth(request):
    return get_view_name_by_path(request.path)
#   pth

def reqValidation(json,keys):
    validReq = True
    for key in keys:
        if(key not in json):
            validReq = False
            break
    return validReq
#   def

def connectDB():
    con = psycopg2.connect(
        dbname   = pgDbName,
        user     = pgUser,
        host     = pgHost,
        password = pgPassword,
        port     = pgPort,
    )
    return con

def disconnectDB(con):
    if(con):
        con.close()
        # is email overlaped
def emailExists(email):
    myCon = connectDB()
    userCursor = myCon.cursor()
    userCursor.execute('SELECT COUNT(*) FROM "f_user" WHERE "email" = %s', (email,))
    result = userCursor.fetchone()
    userCursor.close()
    disconnectDB(myCon)
    return result[0] > 0