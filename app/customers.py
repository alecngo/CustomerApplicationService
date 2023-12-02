from flask import request
from .utils import MongoAPI

class CustomersMongoAPI(MongoAPI):
    def __init__(self):
        super().__init__('customers')  # Initialize the superclass with the 'customers' collection name
        self.required_fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'zipcode']
        self.create_index('email', unique=True)  # Ensure email is unique

    def post(self):
        data = request.get_json()
        return super().post(data)

    def get(self, customer_id=None):
        if customer_id:
            return super().get(customer_id)
        customer_id = request.args.get('_id')
        return super().get(customer_id)

    def put(self):
        data = request.get_json()
        return super().put(data)

    def delete(self):
        customer_id = request.args.get('_id')
        return super().delete(customer_id)