# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4wmjf*dz_0021s#d2r_%*yjj3a-vl08p&8^ftg=k2!6%&ky+p('

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases\

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'TrainK',
		'USER': 'TrainK',
		'PASSWORD': 'v0O7%H&NeShFOy8@cDgO',
		'HOST': 'localhost',
	}
}
