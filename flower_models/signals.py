import telegram
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from flowers.settings import TELEGRAM_TOKEN, CHAT_ID_ADMINISTRATOR, CHAT_ID_COURIER
from .models import Order

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
