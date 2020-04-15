from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore

db = SQLAlchemy()
bcrypt = Bcrypt()
