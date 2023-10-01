import sqlite3

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from queries import *


def generate_send_contact_button():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn = KeyboardButton(text="Kontaktingizni jo'nating: 📞", request_contact=True)
    markup.add(btn)
    return markup


def generate_submitting_buttons():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton(text="Tasdiqlash ✅")
    btn2 = KeyboardButton(text="Rad etish ❌")
    markup.add(btn1, btn2)
    return markup


def generate_main_menu_buttons():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton(text="Menu 📓")
    btn2 = KeyboardButton(text="Buyurtmalarim 🚚")
    btn3 = KeyboardButton(text="Izox qoldirish 💬")
    btn4 = KeyboardButton(text="Sozlamalar ⚙️")

    markup.add(btn1, btn2, btn3, btn4)
    return markup


def generate_categories_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*get_all_categories())

    btn_cart = KeyboardButton(text='Korzina 🛒')
    btn_back = KeyboardButton(text='Ortga ⬅')
    markup.row(btn_cart, btn_back)
    return markup


def generate_products_menu(category_name):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(*get_all_products_from_categories(category_name))
    btn_back = KeyboardButton(text='Ortga ⬅⬅')
    btn_cart = KeyboardButton(text='Korzina 🛒')
    markup.row(btn_cart, btn_back)
    return markup


def generate_cart_back_buttons():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn_cart = KeyboardButton(text="Korzina 🛒")
    btn_back = KeyboardButton(text="Ortga ⬅⬅⬅")
    markup.add(btn_cart, btn_back)
    return markup


def generate_pagination_buttons(product_id, count=1):
    markup = InlineKeyboardMarkup()
    btn_plus = InlineKeyboardButton(text="➕", callback_data=f"change_{product_id}_{count + 1}")
    btn_count = InlineKeyboardButton(text=f"{str(count)}", callback_data="count")
    btn_minus = InlineKeyboardButton(text="➖", callback_data=f"change_{product_id}_{count - 1}")
    btn_cart = InlineKeyboardButton(text="Korzinaga qoshish 🛒", callback_data=f"add_{product_id}_{count}")

    markup.row(btn_minus, btn_count, btn_plus)
    markup.row(btn_cart)
    return markup


def generate_cart_inline(cart_id: int):
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton(text='Ortga ⬅', callback_data='back')
    clear_cart = InlineKeyboardButton(text='Korzinani tozalash ❌', callback_data='clear')
    submit_order = InlineKeyboardButton(text='Zakazni tasdiqlash 🚖', callback_data=f'order_{cart_id}')
    markup.row(submit_order)
    markup.row(clear_cart)
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
    SELECT product_name, cart_product_id
    FROM cart_products
    WHERE cart_id = ?""", (cart_id,))
    cart_products = cursor.fetchall()
    for product_name, product_id in cart_products:
        markup.row(InlineKeyboardButton(text=f'❌ {product_name}', callback_data=f'delete_{product_id}'))
    markup.row(btn_back)
    return markup


def generate_settings_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(text='Telefon raqamingizni yangilang: 📞', request_contact=True)
    btn2 = KeyboardButton(text='Ismingizni yangilang 👤: ')
    btn3 = KeyboardButton(text='uzb🇺🇿')
    btn4 = KeyboardButton(text='ru🇷🇺')
    btn5 = KeyboardButton(text='eng🇺🇸')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def generate_drinks_button():
    markup = ReplyKeyboardMarkup
    btn1 = KeyboardButton(text='Qaynoq ichimliklar')
    btn2 = KeyboardButton(text='Yahna ichimliklar')
    markup.add(btn1, btn2)
    return markup
