from django.db.models.signals import post_save
from django.dispatch import receiver
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CallbackQueryHandler
from .models import Order
from environs import Env


env = Env()
env.read_env()

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')
CHAT_ID_ADMINISTRATOR = env('CHAT_ID_ADMINISTRATOR')
CHAT_ID_COURIER = env('CHAT_ID_COURIER')
bot = telegram.Bot(token=TELEGRAM_TOKEN)


@receiver(post_save, sender=Order)
def notify_telegram(sender, instance, created, **kwargs):
    keyboard = [
        [InlineKeyboardButton('Согласовать заказы', callback_data='collect_orders')],
    ]
    if created:
        message = f"Новый заказ для клиента: {instance.client}, Телефон: {instance.client.phone}, Адрес: {instance.address}, День доставки: {instance.delivery_date}, Букет: {instance.bouquet}"
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=CHAT_ID_ADMINISTRATOR, text=message, reply_markup=reply_markup)


@receiver(post_save, sender=Order)
def notify_courier_on_status_change(sender, instance, **kwargs):
    keyboard = [
        [InlineKeyboardButton('Заказы к доставке', callback_data='all_orders')],
    ]
    if instance.status == "courier":
        message = f"Заказ {instance.id} для клиента {instance.client} по адресу {instance.address} собран и готов к отправке."
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=CHAT_ID_COURIER, text=message, reply_markup=reply_markup)
