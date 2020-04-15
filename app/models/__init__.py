from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_bcrypt import Bcrypt  # NOQA

db = SQLAlchemy()
bcrypt = Bcrypt()
