from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
load_dotenv() 