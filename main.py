import sqlite3

from telebot import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove, LabeledPrice

from configs import *
from keyboards import *
from queries import *

bot = TeleBot(TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    users = get_all_users()
    if chat_id not in users:
        bot.send_message(chat_id, f"""<b>Salom botga xush kelibsiz😊
Botdan foydalanish uchun <i>registratsiyadan</i> o'ting🔖</b>""")
        ask_user_full_name(message)
    else:
        user_data = get_user_data(chat_id)
        bot.send_message(chat_id, f"""Salom 😊 <b>{user_data[2]}</b>, botimizga xush kelibsiz!""")
        main_menu(message)


def ask_user_full_name(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""<b>Ism familyangizni</b> to'liq kiriting: 🧍‍♂️""")
    bot.register_next_step_handler(msg, ask_user_contact)


def ask_user_contact(message: Message):
    chat_id = message.chat.id
    full_name = message.text
    msg = bot.send_message(chat_id, f"""Kontaktingizni jo'nating: 📞""", reply_markup=generate_send_contact_button())
    bot.register_next_step_handler(msg, submitting_user_info, full_name)


def submitting_user_info(message: Message, full_name):
    chat_id = message.chat.id
    contact = message.contact.phone_number
    msg = bot.send_message(chat_id, f"""Ma'lumotlaringizni tasdiqlang:
Ism,familya: {full_name}🤵
Kontakt: {contact}📞""", reply_markup=generate_submitting_buttons())
    bot.register_next_step_handler(msg, check_user_answer, full_name, contact)


# def check_user_answer(message: Message, full_name, contact):
#     chat_id = message.chat.id
#     if message.text == "Tasdiqlash ✅":
#
#         main_menu(message)
#         insert_user_to_users(chat_id, full_name, contact)
#
#
#     elif message.text == "Rad etish ❌":
#         bot.send_message(chat_id, f"""<b>Ma'lumotlar rad etildi. Iltimos qaytadan registratsiyadan o'ting📝</b>""",
#                          reply_markup=ReplyKeyboardRemove())
#         ask_user_full_name(message)
def check_user_answer(message: Message, full_name, contact):
    chat_id = message.chat.id
    if message.text == "Tasdiqlash ✅":
        insert_user_to_users(chat_id, full_name, contact)
        bot.send_message(chat_id, f'<b>Registratsiyadan muvoffaqiyatli o\'tildi ✅</b>',
                         reply_markup=ReplyKeyboardRemove())
        create_cart_for_user(chat_id)
        main_menu(message)

    elif message.text == "Rad etish ❌":
        bot.send_message(chat_id, f"""<b>Registratsiya rad etildi ❌
Botdan foydalanish uchun oldin ro'yxatdan o'ting 📃</b>""",
                         reply_markup=ReplyKeyboardRemove())
        ask_user_full_name(message)


def main_menu(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f"""Menu tanlang va tugmani bosing!""",
                           reply_markup=generate_main_menu_buttons())
    bot.register_next_step_handler(msg, check_user_answer_menu)


def check_user_answer_menu(message: Message):
    if message.text == 'Menu 📓':
        menu(message)
    # elif message.text == "Sozlamalar ⚙":
    #     settings(message)
    elif "⚙" in message.text:
        settings(message)
    elif message.text == "Buyurtmalarim 🚚":
        my_orders(message)
    elif message.text == "Izox qoldirish 💬":
        leave_feedback(message)


def menu(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, """<b>Kategoriyani tanlang: </b>""", reply_markup=generate_categories_buttons())
    bot.register_next_step_handler(msg, check_user_answer_category)


def check_user_answer_category(message: Message):
    chat_id = message.chat.id
    if '⬅' in message.text:
        main_menu(message)
    elif '🛒' in message.text:
        bot.send_message(chat_id, '<b>Korzinani tekshiring: 🛒</b>')
        show_cart(message)
    elif message.text in get_all_categories():
        category = message.text
        product_menu(message, category)
    else:
        main_menu(message)


def product_menu(message: Message, category_name):
    chat_id = message.chat.id
    category_image = get_category_image(category_name)
    with open(category_image, mode='rb') as img:
        msg = bot.send_photo(chat_id, img, f"""<b>Siz tanlagan kategoriya {category_name}</b>""",
                             reply_markup=generate_products_menu(category_name))
        bot.register_next_step_handler(msg, check_user_answer_product, category_name)


def check_user_answer_product(message: Message, category_name):
    if message.text in get_all_products_from_categories(category_name):
        product_name = message.text
        product_detail(message, product_name, category_name)
    elif '⬅⬅' in message.text:
        menu(message)
    else:
        main_menu(message)


def product_detail(message: Message, product_name, category_name):
    chat_id = message.chat.id
    data = get_product_data(product_name)

    with open(data[2], 'rb') as img:
        bot.send_message(chat_id, """<b>Sizning tanlovingiz 👇🏻:</b>""", reply_markup=generate_cart_back_buttons())
        msg = bot.send_photo(chat_id, img, caption=f"<b>{data[4]}\n\nNarxi: {data[3]} sum</b>",
                             reply_markup=generate_pagination_buttons(data[0]))
        bot.register_next_step_handler(msg, check_user_answer_detail, category_name)


def check_user_answer_detail(message: Message, category_name):
    chat_id = message.chat.id
    if '⬅⬅⬅' in message.text:
        product_menu(message, category_name)
    elif '🛒' in message.text:
        bot.send_message(chat_id, """<b>Korzinani tekshiring 🛒</b>""")
        show_cart(message)
    else:
        main_menu(message)


@bot.callback_query_handler(lambda call: 'change' in call.data)
def change_quantity_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = int(call.data.split("_")[1])
    quantity = int(call.data.split("_")[2])
    message_id = call.message.message_id

    if quantity > 0:
        bot.edit_message_reply_markup(chat_id, message_id,
                                      reply_markup=generate_pagination_buttons(product_id, quantity))


@bot.callback_query_handler(func=lambda call: 'add' in call.data)
def add_product_to_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_id = int(call.data.split("_")[1])
    quantity = int(call.data.split("_")[2])

    product_data = get_product_name_price(product_id)

    product_name = product_data[0]
    product_price = int(product_data[1])
    final_price = quantity * product_price

    user_id = get_user_id_from_chat_id(chat_id)
    cart_id = get_cart_id(user_id)
    category_name = get_category_name(product_id)

    database = sqlite3.connect('project.db')
    cursor = database.cursor()

    try:

        cursor.execute("""
            INSERT INTO cart_products(cart_id,product_name,product_quantity,final_price)
            VALUES(?,?,?,?)""", (cart_id, product_name, quantity, final_price))
        database.commit()
    except:

        old_data = get_old_data_abt_product(cart_id, product_name)
        old_quantity = int(old_data[0])
        old_final_price = int(old_data[1])
        new_quantity = old_quantity + quantity
        new_final_price = old_final_price + final_price
        cursor.execute("""
            UPDATE cart_products
            SET product_quantity = ?,
            final_price = ?
            WHERE cart_id = ? AND product_name = ?""",
                       (new_quantity, new_final_price, cart_id, product_name))
        database.commit()
    finally:

        cursor.execute("""
            UPDATE carts
            SET total_price = (SELECT sum(final_price) FROM cart_products WHERE cart_id = ?)
            WHERE cart_id = ?""", (cart_id, cart_id))
        database.commit()
        bot.answer_callback_query(call.id, f"{product_name}\n{quantity} dona korzinaga qo'shildi !", show_alert=True)
        bot.delete_message(chat_id, message_id)
        product_menu(call.message, category_name)
        database.close()


def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = get_user_id_from_chat_id(chat_id)
    cart_id = get_cart_id(user_id)
    total_price = get_total_price(cart_id)
    if total_price > 0:
        cart_products = get_cart_products(cart_id)
        text = generate_cart_text(total_price, cart_products)
        if edit_message:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=generate_cart_inline(cart_id))
        else:
            bot.send_message(chat_id, text, reply_markup=generate_cart_inline(cart_id))
    else:
        bot.send_message(chat_id, f"""<b>Sizning korzinangiz bo'sh ❌</b>""")
        main_menu(message)


@bot.callback_query_handler(func=lambda call: 'back' in call.data)
def back_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.delete_message(chat_id, message_id)
    menu(call.message)  # category_menu


@bot.callback_query_handler(lambda call: 'delete' in call.data)
def delete_product_from_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    message = call.message

    cart_product_id = call.data.split('_')[1]
    user_id = get_user_id_from_chat_id(chat_id)
    cart_id = get_cart_id(user_id)

    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
    DELETE FROM cart_products
    WHERE cart_product_id = ? AND cart_id = ?
    """, (cart_product_id, cart_id))

    database.commit()
    cursor.execute("""
     SELECT sum(final_price)
     FROM cart_products WHERE cart_id = ?""", (cart_id,))
    total_price = cursor.fetchone()[0]
    database.commit()
    cursor.execute("""
        UPDATE  carts
        SET total_price = ? WHERE cart_id = ?""", (total_price, cart_id))
    database.commit()
    database.close()
    bot.answer_callback_query(call.id, f"Mahsulot korzinadan o'chirildi !", show_alert=True)

    show_cart(message, edit_message=True)


@bot.callback_query_handler(lambda call: 'clear' in call.data)
def clear_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = get_user_id_from_chat_id(chat_id)
    cart_id = get_cart_id(user_id)

    bot.delete_message(chat_id, message_id)
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        DELETE FROM cart_products WHERE cart_id = ?""", (cart_id,))
    database.commit()
    cursor.execute("""
        UPDATE carts
        SET total_price = ?
        WHERE cart_id = ?""", (0, cart_id))
    database.commit()
    database.close()
    bot.send_message(chat_id, f"""<b>Sizning korzinangiz bo'sh ❌</b>""")

    main_menu(call.message)


@bot.callback_query_handler(lambda call: 'order' in call.data)
def submit_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = get_user_id_from_chat_id(chat_id)
    cart_id = get_cart_id(user_id)
    total_price = get_total_price(cart_id)
    cart_products = get_cart_products(cart_id)

    text = f""""""
    i = 0
    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f"""{i}.{product_name}
Soni: {quantity}
Narxi: {final_price} so'm\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"""

    text += f"""\n\n\n\n\n\n\n\n\nUmumiy narxi: {total_price} so'm
    
Dostavka: 10000 so'm
Hammasi: {total_price + 10000} """
    bot.delete_message(chat_id,call.message.message_id)
    bot.send_invoice(
        chat_id=chat_id,
        title=f'Sizning chekingiz: №{cart_id}\n\n',
        description=text,
        invoice_payload='bot-defined invoice payload',
        provider_token='371317599:TEST:1692633922324',
        currency= 'UZS',
        prices = [
            LabeledPrice(label='Umumiy narxi:',amount=int(str(total_price) +'00')),
            LabeledPrice(label='Dostavka:' ,amount=1000000)
        ]
    )


def my_orders(message: Message):
    pass


def settings(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Kategoriyani tanglang: ', reply_markup=generate_settings_buttons())
    bot.register_next_step_handler(msg, settings_details)


def settings_details(message: Message):
    chat_id = message.chat.id
    if '👤' in message.text:
        msg = bot.send_message(chat_id, 'Ismingizni qayta kiriting:', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, update_name)
    else:
        main_menu(message)


def update_name(message: Message):
    chat_id = message.chat.id
    update_fullname = message.text
    update_user_full_name(chat_id, update_fullname)
    bot.send_message(chat_id, 'Ismingiz yangilandi!!')
    command_start(message)


def leave_feedback(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "<b>Izoh qoldiring ✍️</b>", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, send_feedback)


def send_feedback(message: Message):
    chat_id = message.chat.id
    user_feedback = message.text
    user_date = get_user_data(chat_id)
    bot.send_message(CHANNEL_ID, f"""<b>Ism,familya: {user_date[2]}
Telefon raqam: {user_date[3]}
Username:{"t.me/" + message.from_user.username}
Izoh :
-----------------------------
{user_feedback}
</b>""")
    bot.send_message(chat_id, f"""<b>Izoh uchun rahmat! ✅</b>""")
    main_menu(message)


bot.polling(none_stop=True)
