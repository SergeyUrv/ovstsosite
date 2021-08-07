SECRET_KEY = '4sD^Cbh|W90jTKZ^6Wv03;2BX4/r&qPUWWjC0Sp`Q5/!#9%|#t'
ALLOWED_HOSTS = ['77.222.42.56', '127.0.0.1', 'altesk.ru']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'btre_prod',
        'USER': 'dbadmin',
        'PASSWORD': 'fzYW9raRMYI3mk8PTa0P',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
DEBUG = False

#add email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@urvachev.ru'
EMAIL_HOST_PASSWORD = 'Jheag%734Hdgb!2'
DEFAULT_FROM_EMAIL = 'Бот ОВсТСО <no-reply@urvachev.ru>'