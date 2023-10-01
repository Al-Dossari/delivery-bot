import sqlite3

database = sqlite3.connect("project.db")
cursor = database.cursor()

#
# --------------------------USER TABLE -----------------------------------------------
# database = sqlite3.connect("project.db")
# cursor = database.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users(
#     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     telegram_id INTEGER UNIQUE,
#     full_name TEXT,
#     contact TEXT
#     )""")

# --------------------------CATEGORIES TABLE--------------------------------------------
# database = sqlite3.connect("project.db")
# cursor = database.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS categories(
#     category_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     category_name TEXT,
#     category_photo TEXT)
# """)

# cursor.execute("""
#     INSERT OR IGNORE INTO categories(category_name,category_photo)
#     VALUES
#     ('Burgers','images/categories/burgers.jpg'),
#     ('Haggi','images/categories/haggi.jpg'),
#     ('Hotdogs','images/categories/hotdogs.jpg'),
#     ('Drink','images/categories/icedrink.jpg'),
#     ('Klabsendvich','images/categories/kalbsendvich.jpg'),
#     ('Lavash','images/categories/lavash.jpg'),
#     ('Pizza','images/categories/pizza.jpg'),
#     ('Salat','images/categories/salat.jpg'),
#     ('Snek','images/categories/snek.jpg'),
#     ('Sous','images/categories/sous.jpg'),
#     ('Strips','images/categories/strips.jpg'),
#     ('Setlar','images/categories/set.jpg')
#     """)
#
#
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRiMARY KEY AUTOINCREMENT,
        product_name TEXT UNIQUE,
        product_image TEXT,
        product_price TEXT,
        product_description TEXT DEFAULT "",
        category_id INTEGER REFERENCES categories(category_id)
    )
""")

#
cursor.execute("""
    INSERT OR IGNORE INTO products(product_name,product_image,product_price,product_description,category_id)
    VALUES
    ('Bigburger','images/products/burgerlar/bigburger.jpg','33000',
    "Shirin bulochka, maxsus sous, aysberg, tuzlangan bodring, ikkita mol go`shtidan kotlet, pomidor, Brunswick shirin piyoz halqalari",
    1),
    ('Big Chizburger','images/products/burgerlar/bigchizburger.jpg','37000',
    "Shirin bulochka, maxsus sous, aysberg, tuzlangan bodring, ikkita mol go`shtidan kotlet, pomidor, pishloq, Brunswick shirin piyoz halqalari",
    1),
    ('Big Doner','images/products/burgerlar/big-doner.jpg','26000',
    "Ekmek mualliflik noni, oq va qizil souslar, chiplar, mol go'shti, bodring, pomidor",
    1),
    ('Chizburher','images/products/burgerlar/chizburger.jpg','24000',
    'Shirin bulochka, maxsus sous, aysberg, tuzlangan bodring, mol go`shtidan kotlet, pomidor, pishloq, "Brunswik" shirin piyoz halqalari',
    1),
    ('Gamburger','images/products/burgerlar/gamburger.jpg','22000',
    'Shirin bulochka, maxsus sous, aysberg, tuzlangan bodring, mol go`shtidan kotlet, pomidor, "Brunswick" shirin piyoz halqalari',
    1),
    ('Shaurma','images/products/burgerlar/shaurma.jpg','22000',
    'Tandirli pitsa noni, mol go`shti, bodring, pomidor, qizil sous, "Brunswick" shirin piyoz halqalari',
    1),
    ('Haggi','images/products/haggi/haggi.jpg','31000',
    "Baget noni, mayonez, mol go'shti, salat bargi, bodring, pomidor, pishloq, qizil sous, Brunswick shirin piyoz halqalari",
    2),
    ('Hot-dog','images/products/hot-doglar/hot-dog.jpg','11000',
    'Yumshoq bulochka, sosiska, ketchup, mayonez, ikra, bodring, pomidor',
    3),
    ('Pishloqli Hot-dog','images/products/hot-doglar/cheese-hot-dog.jpg','14000',
    ' Hot-dog bulochkasi, maxsus sous, tuzlangan bodring, pomidor, pishloq sousi, salat bargi, sosiska',
    3),
    ('Shohona Hot-dog','images/products/hot-doglar/shoxona-hot-dog.jpg','21000',
    ' Hot-dog bulochkasi, maxsus sous, tuzlangan bodring, pomidor, pishloq sousi, pishloq, salat bargi, ikkita sosiska',
    3),

    ('Klab sendvich','images/products/klab-sendvich/klab-sendvich.jpg','30000',
    'Toster non, maxsus sous, bodring, pomidor, tovuq filesi, salat bargi, pishloq, kartoshka fri',5),

    ('Orginal lavash','images/products/lavash/original-lavash.jpg','28000',
    "'Yupqa lavash non, pomidor, chips, mol go'shti, qizil sous, mayonez",6),
    ('Pishloqli lavash','images/products/lavash/cheese-lavash.jpg','31000',
    "Yupqa lavash non, pomidor, chips, mol go'shti, qizil sous, mayonez, pishloq.",6),
    ('Pishloqli tandir lavash','images/products/lavash/cheese-tandir-lavash.jpg','32000',
    "Tandirda pishirilgan yupqa lavash non, pomidor, chips, mol go'shti, pishloq, qizil sous, mayonez, kunjut.",6),
    ('Pishloqli mini lavash','images/products/lavash/mini-cheese-lavash.jpg','26000',
    "Yupqa lavash non, pomidor, chips, mol go'shti, qizil sous, mayonez, pishloq.",6),
    ('Mini orginal lavash','images/products/lavash/mini-original-lavash.jpg','23000',
    "Yupqa lavash non, pomidor, chips, mol go'shti, qizil sous, mayonez, pishloq.",6),
    ('Tandir lavash','images/products/lavash/tandir-lavash.jpg','29000',
    "Tandir pechida pishirilgan yupqa lavash non, pomidor, chips, mol go'shti, qizil sous, mayonez, kunjut.",6),

    ('Assorti pitsa','images/products/pizza/assorti-pitsa.jpg','89000',
    "Oq sous, zaytun, qo'ziqorin, bulg'or qalampiri, pomidor, dudlangan kurka, dudlangan kolbasa, mol go'shti, sosiska,
    Mozzarella va Akbel pishloqlari.",7),
    ("Go'shtli pitsa",'images/products/pizza/goshtli-pitsa.jpg','87000',
    'Tomato sauce “OQTEPA”, chicken meat, bell pepper, beef, tomatoes, Mozzarella and Akbel cheese',7),
    ('Peppironi pitsa','images/products/pizza/peppironi-pitsa.jpg','75000',
    "OQTEPA” pomidor sousi, dudlangan kolbasa, Mozzarella va Akbel pishlog'i",7),
    ('Qazili pitsa','images/products/pizza/qazili-pitsa.jpg','90000',
    'OQTEPA” pomidor sousi, "Brunswick" shirin piyoz halqalari, qazi, Mozzarella va Akbel pishloqlari',7),
    ('Tovuqli pitsa','images/products/pizza/tovuqli-pitsa.jpg','75000',
    "OQTEPA pomidor sousi, kurka, tovuq, qo'ziqorin, zaytun, pishloq, oregano",7),

    ('Bayts','images/products/qarsildoq-jojalar/bayts.jpg','16000',
    "Qarsildoq panirovkadagi tovuq bo'laklari",11),
    ("Jo'ja box",'images/products/qarsildoq-jojalar/joja-box.jpg','26000',
    "Strips 3 dona, kartoshka fri o'rta va ketchup",11),
    ('Stips 3 dona','images/products/qarsildoq-jojalar/stips-3-dona.jpg','16000',
    "Qarsildoq panirovkadagi uzun shaklda kesilgan tovuq bo'laklari",11),
    ('Stips 5 dona','images/products/qarsildoq-jojalar/stips-5-dona.jpg','26000',
    "Qarsildoq panirovkadagi uzun shaklda kesilgan tovuq bo'laklari",11),

    ('Mujskoy kapriz','images/products/salatlar/mujskoy-kapriz.jpg','25000',
    'Dudlangan kolbasa, kurka, qazi, pishloq, mayonez',8),
    ('Sezar','images/products/salatlar/sezar.jpg','23000',
    'Tovuq filesi, pomidor, aysberg, pishloq, kruton, sarimsoq sousi.',8),

    ('Set Baraka','images/products/setlar/set-baraka.jpg','134000',
    "Assorti pitsa, kartoshka fri o'rta 3 dona, Pepsi 0.4L 3 dona, ketchup 3 dona",12),
    ('Set Juftlik','images/products/setlar/set-juftlik.jpg','58000',
    'Klab sendvich, strips 3 dona, Pepsi 0.4L 2 dona, ketchup 2 dona',12),
    ('Set Oqtepa','images/products/setlar/set-oqtepa.jpg','17000',
    "Kartoshka fri o'rta, Pepsi 0.4L",12),

    ('Jaydari fri','images/products/sneklar/jaydari-fri.jpg','15000','Jaydari kartoshka',9),
    ('Kartoshka fri','images/products/sneklar/kartoshka-fri.jpg','14000',"Kartoshka fri o'rta",9),
    ('Big kartoshka fri','images/products/sneklar/kartoshka-fri-big.jpg','18000','Kartoshka fri katta',9),
    ('Mini kartoshka fri','images/products/sneklar/kartoshka-fri-mini.jpg','8000','Kartoshka fri kichkina',9),
    ('Non','images/products/sneklar/non.jpg','3000','non',9),
    ('Xalapenyo','images/products/sneklar/xalapenyo.jpg','3000','Xalapenyo',9),

    ('Chili sous','images/products/souslar/chili-sous.jpg','3000','Chili sous',10),
    ('Ketchup','images/products/souslar/ketchup.jpg','3000','Ketchup',10),
    ('Oq sous','images/products/souslar/oq-sous.jpg','3000','Oq sous',10),
    ('Pishloqli sous','images/products/souslar/pishloqli-sous.jpg','3000','Pishloqli sous',10);
    """)


#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS carts(
#         cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER REFERENCES users(user_id),
#         total_price INTEGER DEFAULT 0
#     );
# """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS cart_products(
#         cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         cart_id INTEGER REFERENCES carts(cart_id),
#         product_name TEXT UNIQUE,
#         product_quantity INTEGER,
#         final_price INTEGER);""")
database.commit()
database.close()
