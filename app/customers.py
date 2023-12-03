from bson import ObjectId
from flask import jsonify, request
from .utils import MongoAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomersMongoAPI(MongoAPI):
    def __init__(self):
        super().__init__('customers')  # Initialize the superclass with the 'customers' collection name
        self.required_fields = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'zipcode']
        self.allowed_statuses = ['Pending', 'Rejected', 'Approved']
        self.create_index('email', unique=True)  # Ensure email is unique

    def post(self):
        data = request.get_json()
        return super().post(data)

    def get(self, customer_id=None):
        if not customer_id:
            customer_id = request.args.get('_id')
        return super().get(customer_id)

    def put(self, data=None):
        logger.info("Customer Data in CustomersMongoAPI: %s", data)
        if not data:
            data = request.get_json()

        if 'customer_id' in data and 'animal_id' in data:
            if data.get('delete_application'):
                return self.delete_application(data)
            else:
                return self.handle_application_update(data)
        
        # Standard customer update logic
        if '_id' not in data:
            return jsonify({"error": "Missing _id parameter"}), 400
        customer_id = data['_id']
        try:
            query = {"_id": ObjectId(customer_id)}
        except Exception:
            return jsonify({"error": "Invalid _id format"}), 400

        data.pop('_id', None)
        updated_data = {"$set": data}
        result = self.collection.update_one(query, updated_data)
        if result.modified_count > 0:
            return jsonify({"message": "Customer updated successfully"}), 200
        else:
            return jsonify({"error": "Document not found or data unchanged"}), 404

    def handle_application_update(self, data, new_status="Pending"):
        customer_id = data['customer_id']
        animal_id = data['animal_id']
        if data.get('new_status'):
            new_status = data['new_status']

        if new_status not in self.allowed_statuses:
            return jsonify({"error": "Invalid status"}), 400

        response, status_code = super().get(customer_id)
        if status_code != 200:
            return response, status_code

        customer_data = response.get_json()
        
        # Add or update the application in the customer data
        application = {'status': new_status}
        if 'applications' not in customer_data:
            customer_data['applications'] = {animal_id: application}
        else:
            customer_data['applications'][animal_id] = application

        customer_data['_id'] = customer_id
        return super().put(customer_data)

    def delete_application(self, data):
        customer_id = data['customer_id']
        animal_id = data['animal_id']

        response, status_code = super().get(customer_id)
        if status_code != 200:
            return response, status_code

        customer_data = response.get_json()

        # Delete the application with the given animal_id
        if 'applications' in customer_data and animal_id in customer_data['applications']:
            del customer_data['applications'][animal_id]
        else:
            return jsonify({"error": "Application not found"}), 404

        customer_data['_id'] = customer_id
        return super().put(customer_data)
    
    def delete(self):
        customer_id = request.args.get('_id')
        return super().delete(customer_id)