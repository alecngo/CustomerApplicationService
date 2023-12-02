from flask import jsonify, request
from datetime import datetime
from .utils import MongoAPI
from .customers import CustomersMongoAPI
from .animals import AnimalsMongoAPI

class ApplicationsMongoAPI(MongoAPI):
    def __init__(self):
        super().__init__('applications')
        self.required_fields = ['customer_id', 'animal_id', 'status']
        self.allowed_statuses = ['Pending', 'Rejected', 'Approved']
        self.customer_api = CustomersMongoAPI()
        self.animal_api = AnimalsMongoAPI()

    def post(self):
        data = request.get_json()
        error = self.validate_application(data)
        if error:
            return jsonify({"success": False, "message": error}), 400

        data['date_created'] = datetime.utcnow()
        return super().post(data)

    def get(self, application_id=None):
        if application_id:
            return super().get(application_id)
        application_id = request.args.get('_id')
        return super().get(application_id)
    
    def put(self):
        data = request.get_json()
        application_id = data.get('_id')
        new_status = data.get('status')

        if not application_id or new_status not in self.allowed_statuses:
            return jsonify({"success": False, "message": "Invalid data"}), 400

        return super().put(data)

    def delete(self):
        application_id = request.args.get('_id')
        return super().delete(application_id)

    def validate_application(self, data):
        if not all(field in data for field in self.required_fields):
            missing_fields = [field for field in self.required_fields if field not in data]
            return f"Missing fields: {', '.join(missing_fields)}"

        _, customer_api_code = self.customer_api.get(customer_id=data['customer_id'])
        if customer_api_code != 200:
            return f"Customer with ID {data['customer_id']} does not exist."

        _, animal_api_code = self.animal_api.get(animal_id=data['animal_id'])
        if animal_api_code != 200:
            return f"Animal with ID {data['animal_id']} does not exist."

        if data['status'] not in self.allowed_statuses:
            return f"Invalid status. Allowed statuses are: {', '.join(self.allowed_statuses)}"
        return None
