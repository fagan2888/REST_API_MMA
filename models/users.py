from flask_sqlalchemy import SQLAlchemy
import datetime

from . import db, bcrypt

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)

	def __init__(self, email, password):
		self.email = email
		self.password = self.__generate_hash(password)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self, email, password):
		self.email = email
		self.password = self.__generate_hash(password)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	@staticmethod
	def get_all_users():
		return User.query.all()

	@staticmethod
	def get_one_user(id):
		return User.query.get(id)

	@staticmethod
	def get_user_by_email(value):
		return User.query.filter_by(email=value).first()

	def __generate_hash(self, password):
		return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

	def check_hash(self, password):
		return bcrypt.check_password_hash(self.password, password)

	def __repr(self):
		return f'<id {self.id}>'

	def serialize(self):
	    return {
	        'id': self.id,
	        'email': self.email,
	    }