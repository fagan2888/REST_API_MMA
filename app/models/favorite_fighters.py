from . import db  # type: ignore


class FavoriteFighter(db.Model):
    __tablename__ = 'favorite_fighters'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    fighter_name = db.Column(db.String(128), primary_key=True, nullable=False)

    def __init__(self, user_id, fighter_name):
        self.user_id = user_id
        self.fighter_name = fighter_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, user_id, fighter_name):
        self.user_id = user_id
        self.fighter_name = fighter_name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_fighters():
        return FavoriteFighter.query.all()

    @staticmethod
    def get_fighter(user_id, fighter_name):
        return FavoriteFighter.query.filter_by(
            user_id=user_id, fighter_name=fighter_name).first()

    @staticmethod
    def get_one_fighter(user_id):
        return FavoriteFighter.query.get(user_id)

    def __repr(self):
        return f'<user_id {self.user_id}>'

    def serialize(self):
        return {
            'user_id': self.user_id,
            'fighter_name': self.fighter_name,
        }
