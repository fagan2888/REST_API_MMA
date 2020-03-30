from models.users import User
from . import db

class FavoriteFighter(db.Model):
	__tablename__ = 'favorite_fighters'

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
	fighter_name = db.Column(db.String(128), primary_key=True, nullable=False)

	def __init__(self, fighter_name):
		self.fighter_name = fighter_name

	def save(self):
		db.session.add(self)
		db.session.commit()

	def update(self, fighter_name):
		self.fighter_name = fighter_name
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

	def __repr(self):
		return f'<id {self.user_id}>'

	def serialize(self):
	    return {
	        'id': self.user_id,
	        'fighter_name': self.fighter_name,
	    }