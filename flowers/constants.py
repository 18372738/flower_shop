from environs import Env

env = Env()
env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
CHAT_ID_ADMINISTRATOR = env('CHAT_ID_ADMINISTRATOR')
CHAT_ID_COURIER = env('CHAT_ID_COURIER')
