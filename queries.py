def insert_user_to_users(telegram_id, full_name, contact):
    import sqlite3

    database = sqlite3.connect("project.db")

    cursor = database.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO users(telegram_id,full_name,contact)
    VALUES(?,?,?)""", (telegram_id, full_name, contact))
    database.commit()
    database.close()


def get_all_users():
    import sqlite3
    database = sqlite3.connect("project.db")
    cursor = database.cursor()
    cursor.execute(f"""
    SELECT telegram_id FROM users""")
    users = cursor.fetchall()
    database.close()
    users = [user[0] for user in users]
    return users


def get_user_data(telegram_id):
    import sqlite3
    database = sqlite3.connect("project.db")
    cursor = database.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE telegram_id = ?""", (telegram_id,))
    user_data = cursor.fetchone()
    database.close()

    return user_data


def get_all_categories():
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""SELECT * FROM categories;""")
    categories = cursor.fetchall()
    database.close()
    categories = [category[1] for category in categories]
    return categories


def get_category_image(category_name):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
    SELECT category_photo FROM categories WHERE category_name = ?""", (category_name,))
    category_image = cursor.fetchone()[0]
    database.close()
    return category_image


def get_all_products_from_categories(category_name):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()

    cursor.execute("""
        SELECT product_name FROM products
        WHERE category_id = (SELECT category_id FROM categories WHERE category_name = ?)
        """, (category_name,))
    products = cursor.fetchall()
    database.close()
    products = [product[0] for product in products]
    return products


def get_product_data(product_name):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT * FROM products
        WHERE product_name = ?""", (product_name,))
    product_data = cursor.fetchone()
    database.close()
    return product_data


def create_cart_for_user(chat_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
    SELECT user_id FROM users 
    WHERE telegram_id = ?""", (chat_id,))
    user_id = cursor.fetchone()[0]
    cursor.execute("""
        INSERT INTO carts(user_id)
        VALUES(?)""", (user_id,))
    database.commit()
    database.close()


def update_user_full_name(telegram_id, new_full_name):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
    UPDATE users
    SET full_name = ?
    WHERE telegram_id = ?;
    """, (new_full_name, telegram_id,))
    database.commit()
    database.close()


def get_product_name_price(product_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT product_name,product_price from products
        WHERE product_id = ?""", (product_id,))
    data = cursor.fetchone()
    database.close()
    return data


def get_user_id_from_chat_id(chat_id):
    import sqlite3
    database = sqlite3.connect("project.db")
    cursor = database.cursor()
    cursor.execute("""
        SELECT user_id FROM users
        WHERE telegram_id = ?""", (chat_id,))
    user_id = cursor.fetchone()[0]
    database.close()
    return user_id


def get_cart_id(user_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT cart_id FROM carts 
        WHERE user_id = ?""", (user_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def get_category_name(product_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT category_id FROM products
         WHERE product_id = ?""", (product_id,))
    category_id = cursor.fetchone()[0]
    cursor.execute("""
        SELECT category_name FROM categories
        WHERE category_id = ?""",(category_id,))
    category_name = cursor.fetchone()[0]
    database.close()
    return category_name


def get_old_data_abt_product(cart_id, product_name):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT product_quantity,final_price FROM cart_products
        WHERE cart_id = ? AND product_name = ? """, (cart_id, product_name))
    old_data = cursor.fetchone()
    database.close()
    return old_data


def update_product_in_cart_products(cart_id, product_name, new_quantity, new_final_price):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        UPDATE cart_products
        SET product_quantity = ?,
        final_price = ?
        WHERE cart_id = ? AND product_name = ?""",
                   (new_quantity, new_final_price, cart_id, product_name))
    database.commit()
    database.close()


def get_total_price(cart_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT total_price FROM carts
        WHERE cart_id = ?""", (cart_id,))
    total_price = cursor.fetchone()[0]
    database.close()
    return 0 if total_price is None else total_price


def get_cart_products(cart_id):
    import sqlite3
    database = sqlite3.connect('project.db')
    cursor = database.cursor()
    cursor.execute("""
        SELECT product_name,product_quantity,final_price
        FROM cart_products WHERE cart_id = ?""", (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products


def generate_cart_text(total_price, cart_products: list):
    text = f"<b>Sizning korzinangiz: \n\n</b>"
    i = 0
    for product_name, quantity, final_price in cart_products:
        i += 1
        text += f"""<b>{i}.{product_name}
Soni: {quantity}
Narxi: {final_price} so'm 💰\n\n</b>"""

    text += f"""<b>Umumiy narxi: {total_price} so'm 💰
Dostavka: 10000 so'm 💵
Hamasi: {total_price + 10000} so'm 💰</b>"""
    return text
