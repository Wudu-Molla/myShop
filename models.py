# import psycopg2
#
# connection = psycopg2.connect(
#     host='localhost',
#     port='5432',
#     user='wudu',
#     password='Wm867943322',
#     database='shop'
# )
#
# cursor = connection.cursor()
# cursor.execute('SELECT version()')
# db_version = cursor.fetchone()
# print(db_version)
# cursor.close()
# #

from shop import db
from flask_login import UserMixin


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(256), nullable=False)
    barcode = db.Column(db.String(24), nullable=False, unique=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(512), nullable=False)
    size = db.Column(db.String(48), nullable=False)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}, barcode: {self.barcode}, description: {self.description}, ' \
               f'Image: {self.image}, price: {self.price}, size: {self.size}'


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'id: {self.id}, email: {self.email}'


class Cart(db.Model):
    pass
