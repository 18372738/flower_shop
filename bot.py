import os
import sys
import telegram
import django
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, CallbackQuery
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowers.settings')
django.setup()

from flower_models.models import Event, Bouquet, Client, Order, Consultation

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID_ADMINISTRATOR = os.environ['CHAT_ID_ADMINISTRATOR']
CHAT_ID_COURIER = os.environ['CHAT_ID_COURIER']


def start(update: Update, context: CallbackContext) -> None:
    telegram_id = str(update.effective_user.id)
    if telegram_id == str(CHAT_ID_ADMINISTRATOR):
        show_main_menu_admin(update.message)
    elif telegram_id == str(CHAT_ID_COURIER):
        show_main_menu_courier(update.message)
    else:
        update.message.reply_text("Данный бот предназначен для сотрудников магазина.")


def show_main_menu_admin(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Новые заказы', callback_data='new_order')],
        [InlineKeyboardButton('Заказы к сборке', callback_data='order_collect')],
        [InlineKeyboardButton('Консультация клиентов', callback_data='consult_client')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Привет! Я бот FlowerShop. Я помогу тебе отслеживать новые заказы и заказы к сборке', reply_markup=reply_markup)


def show_main_menu_courier(message) -> None:
    keyboard = [
        [InlineKeyboardButton('Заказы для доставки', callback_data='remaining_term')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message.reply_text('Добро пожаловать в FlowerShop', reply_markup=reply_markup)


def main_menu_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'new_order':
        show_new_orders(query)
    elif query.data == 'order_collect':
        show_order_collect(query)
    elif query.data == 'remaining_term':
        show_order_delivery(query)
    if query.data == 'collect_orders':
        show_new_orders(query)
    elif query.data == 'all_orders':
        show_order_delivery(query)
    elif query.data == 'consult_client':
        show_consultation_client(query)
    elif query.data == 'consult':
        show_consultation_client(query)


def show_new_orders(query) -> None:
    orders = Order.objects.filter(status="true")
    if orders.exists():
        for order in orders:
            message = f"Заказ #{order.id}, Букет: {order.bouquet}, Клиент: {order.client}, Телефон: {order.client.phone}, Адрес: {order.address}"
            keyboard = [
                [InlineKeyboardButton("Заказ согласован", callback_data=f"agree:{order.id}")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(message, reply_markup=reply_markup)
        keyboard_main_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_main_menu = InlineKeyboardMarkup(keyboard_main_menu)
        query.message.reply_text("Перейти в главное меню", reply_markup=reply_markup_main_menu)
    else:
        keyboard_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_menu = InlineKeyboardMarkup(keyboard_menu)
        query.message.reply_text("Нет новых заказов", reply_markup=reply_markup_menu)


def agree_order(update: Update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data.split(':')[1]
    order = Order.objects.get(id=order_id)
    order.status = "collect"
    order.save()
    query.edit_message_text(f"Заказ #{order.id}, для клиента {order.client}, согласован!")


def show_order_collect(query) -> None:
    orders = Order.objects.filter(status="collect")
    if orders.exists():
        for order in orders:
            message = f"Заказ #{order.id}, Букет: {order.bouquet}, Клиент: {order.client}, Телефон: {order.client.phone}, Адрес: {order.address}"
            keyboard = [
                [InlineKeyboardButton("Заказ собран", callback_data=f"collect:{order.id}")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(message, reply_markup=reply_markup)
        keyboard_main_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_main_menu = InlineKeyboardMarkup(keyboard_main_menu)
        query.message.reply_text("Перейти в главное меню", reply_markup=reply_markup_main_menu)
    else:
        keyboard_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_menu = InlineKeyboardMarkup(keyboard_menu)
        query.message.reply_text("Нет новых заказов", reply_markup=reply_markup_menu)


def collect_order(update: Update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data.split(':')[1]
    order = Order.objects.get(id=order_id)
    order.status = "courier"
    order.save()
    query.edit_message_text(f"Заказ #{order.id}, для клиента {order.client}, собран и направлен курьеру")


def show_order_delivery(query) -> None:
    orders = Order.objects.filter(status="courier")
    if orders.exists():
        for order in orders:
            message = f"Заказ #{order.id}, Букет: {order.bouquet}, Клиент: {order.client}, Телефон: {order.client.phone}, Адрес: {order.address}"
            keyboard = [[InlineKeyboardButton("Заказ доставлен", callback_data=f"courier:{order.id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(message, reply_markup=reply_markup)
        keyboard_main_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_courier")],
        ]
        reply_markup_main_menu = InlineKeyboardMarkup(keyboard_main_menu)
        query.message.reply_text("Перейти в главное меню", reply_markup=reply_markup_main_menu)
    else:
        keyboard_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_courier")],
        ]
        reply_markup_menu = InlineKeyboardMarkup(keyboard_menu)
        query.message.reply_text("Нет заказов к доставке", reply_markup=reply_markup_menu)


def delivery_order(update: Update, context):
    query = update.callback_query
    query.answer()
    order_id = query.data.split(':')[1]
    order = Order.objects.get(id=order_id)
    order.status = "delivered"
    order.save()
    query.edit_message_text(f"Заказ #{order.id}, для клиента {order.client}, доставлен")


def main_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'main_menu_admin':
        show_main_menu_admin(query.message)
    elif query.data == 'main_menu_courier':
        show_main_menu_courier(query.message)


def show_consultation_client(query) -> None:
    consultations = Consultation.objects.filter(consulted=False)
    if consultations.exists():
        for consultation in consultations:
            message = f"Клиент: {consultation.name}. Телефон: {consultation.phone}"
            keyboard = [[InlineKeyboardButton("Проконсультирован", callback_data=f"consulted:{consultation.id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(message, reply_markup=reply_markup)
        keyboard_main_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_main_menu = InlineKeyboardMarkup(keyboard_main_menu)
        query.message.reply_text("Перейти в главное меню", reply_markup=reply_markup_main_menu)
    else:
        keyboard_menu = [
            [InlineKeyboardButton("Главное меню", callback_data="main_menu_admin")],
        ]
        reply_markup_menu = InlineKeyboardMarkup(keyboard_menu)
        query.message.reply_text("Нет клиентов для консультации", reply_markup=reply_markup_menu)


def consultation_conducted(update: Update, context):
    query = update.callback_query
    query.answer()
    consultation_id = query.data.split(':')[1]
    consultation = Consultation.objects.get(id=consultation_id)
    consultation.consulted = True
    consultation.save()
    query.edit_message_text(f"Консультация #{consultation.id} для {consultation.name} проведена.")


if __name__ == '__main__':
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(main_menu_handler, pattern='^(new_order|order_collect|remaining_term|collect_orders|all_orders|consult_client|consult|)$'))
    dispatcher.add_handler(CallbackQueryHandler(agree_order, pattern="^agree:"))
    dispatcher.add_handler(CallbackQueryHandler(collect_order, pattern="^collect:"))
    dispatcher.add_handler(CallbackQueryHandler(delivery_order, pattern="^courier:"))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern="^(main_menu_admin|main_menu_courier|)$"))
    dispatcher.add_handler(CallbackQueryHandler(consultation_conducted, pattern="^consulted:"))
    updater.start_polling()
    print('Бот в сети')
    updater.idle()
