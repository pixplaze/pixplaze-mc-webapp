from flask import Flask
from config import Config
from flask_restful import Api
from api import test_api
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
cors = CORS(app)

api.add_resource(test_api.Usercacahe, '/usercache')

from app import routes
