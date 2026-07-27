from yacut import api_views, views
from yacut import views
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import error_handlers, api_views, views  # noqa: E402, F401