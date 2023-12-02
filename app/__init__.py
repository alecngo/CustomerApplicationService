from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

load_dotenv()

app = Flask(__name__)
api = Api(app)
print("App created")
from .customers import CustomersMongoAPI

app.add_url_rule('/customer', view_func=CustomersMongoAPI.as_view('customer_api'), methods=['POST', 'GET', 'DELETE', 'PUT'])
