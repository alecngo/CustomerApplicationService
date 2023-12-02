from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

load_dotenv()

app = Flask(__name__)
api = Api(app)

from .customers import CustomersMongoAPI
from .animals import AnimalsMongoAPI
from .applications import ApplicationsMongoAPI

app.add_url_rule('/customer', view_func=CustomersMongoAPI.as_view('customer_api'), methods=['POST', 'GET', 'DELETE', 'PUT'])
app.add_url_rule('/animal', view_func=AnimalsMongoAPI.as_view('animal_api'), methods=['POST', 'GET', 'DELETE', 'PUT'])
app.add_url_rule('/application', view_func=ApplicationsMongoAPI.as_view('application_api'), methods=['POST', 'PUT', 'DELETE'])
