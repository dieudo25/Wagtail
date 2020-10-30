from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5a^muwx7xv4kx_y!p1yr$^y#t66zyjxt0v+s%8ozv%f*umjt^k'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    'wagtail.contrib.styleguide'
]

MIDDLEWARE = MIDDLEWARE + [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1', '172.17.0.1')

CACHES = {
    "default": {
        "BACKEND" : "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION" : "/home/dieudo/Dev/Wagtail/mysite/cache"
    }
} 


try:
    from .local import *
except ImportError:
    pass
