import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from models.users import User
from models.favorite_fighters import FavoriteFighter

# from models.models import User, FavoriteFighter

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
