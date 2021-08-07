from .settings import BASE_DIR
SECRET_KEY = '6g=#a*^ido%dw9t0m$vd9lvs!sr68k13*c6_4&pkx9l2a3s79m'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DEBUG = True

#add email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@urvachev.ru'
EMAIL_HOST_PASSWORD = 'Jheag%734Hdgb!2'
DEFAULT_FROM_EMAIL = 'Бот ОВсТСО <no-reply@urvachev.ru>'