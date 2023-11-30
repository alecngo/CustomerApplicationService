from datetime import datetime
from flask import jsonify, request
from .db import customers_collection, applications_collection, animals_collection
from pymongo.errors import DuplicateKeyError
from app import app
from bson import ObjectId


required_fields_to_create_customer = ['email', 'password', 'phone_number', 'first_name', 'last_name', 'zipcode']
required_fields_to_create_animal = ['animal_id', 'rescue_center', 'breed', 'image_url', 'adoptable']
required_fields_to_create_application = ['customer_email', 'animal_id', 'status']
allowed_application_status = ['Pending', 'Rejected', 'Approved']

def validate_and_create_customer_json(data):
    # Check if all required fields are in the data
    if not all(field in data for field in required_fields_to_create_customer):
        missing_fields = [field for field in required_fields_to_create_customer if field not in data]
        return None, f"Missing fields: {', '.join(missing_fields)}"
    
    # Construct the customer JSON object
    customer_json = {
        'email': data['email'],
        'password': data['password'],  # TODO: Hash the password before saving
        'phone_number': data['phone_number'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'zipcode': data['zipcode']
    }
    
    # TODO: Add additional validation if necessary (e.g., email format, password strength)
    
    return customer_json, None

@app.route('/add-customer', methods=['POST'])
def add_customer():
    data = request.get_json()

    customer_json, error = validate_and_create_customer_json(data)
    if error:
        return jsonify({"success": False, "message": error}), 400

    try:
        customers_collection.insert_one(customer_json)
        return jsonify({"success": True, "message": "Customer added"}), 201
    except DuplicateKeyError:
        return jsonify({"success": False, "message": "A customer with this email already exists"}), 409
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

@app.route('/find-customer', methods=['GET'])
def find_customer():
    # Get email from query parameters
    email = request.args.get('email')

    if not email:
        return jsonify({"error": "Missing email parameter"}), 400

    try:
        customer = customers_collection.find_one({"email": email})
        if customer:
            customer_data = {
                "first_name": customer.get("first_name"),
                "last_name": customer.get("last_name"),
                "phone_number": customer.get("phone_number"),
                "zipcode": customer.get("zipcode")
            }
            return jsonify(customer_data), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def validate_and_create_animal_json(data):
    # Check if all required fields are in the data
    if not all(field in data for field in required_fields_to_create_animal):
        missing_fields = [field for field in required_fields_to_create_animal if field not in data]
        return None, f"Missing fields: {', '.join(missing_fields)}"
    
    # Construct the animal JSON object
    animal_json = {
        'animal_id': data['animal_id'],
        'rescue_center': data['rescue_center'],
        'breed': data['breed'],
        'image_url': data.get('image_url', ''),  # Image URL can be optional
        'adoptable': data['adoptable']
    }
    
    # TODO: Add additional validation if necessary
    
    return animal_json, None

@app.route('/add-animal', methods=['POST'])
def add_animal():
    data = request.get_json()
    animal_json, error = validate_and_create_animal_json(data)

    if error:
        return jsonify({"success": False, "message": error}), 400

    try:
        # Check for existing animal with the same animal_id
        if animals_collection.find_one({'animal_id': animal_json['animal_id']}):
            return jsonify({"success": False, "message": "Animal with this ID already exists"}), 409

        result = animals_collection.insert_one(animal_json)
        return jsonify({"success": True, "message": "Animal added", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
def validate_and_create_application_json(data):
    # Check if all required fields are in the data
    if not all(field in data for field in required_fields_to_create_application):
        missing_fields = [field for field in required_fields_to_create_application if field not in data]
        return None, f"Missing fields: {', '.join(missing_fields)}"
    
    # Check if customer exists
    customer_email = data['customer_email']
    if not customers_collection.find_one({"email": customer_email}):
        return None, f"Customer with email {customer_email} does not exist."

    # Check if animal exists
    animal_id = data['animal_id']
    if not animals_collection.find_one({"animal_id": animal_id}):
        return None, f"Animal with ID {animal_id} does not exist."

    # Construct the application JSON object
    application_json = {
        'customer_email': customer_email,
        'animal_id': animal_id,
        'status': data['status'],
        'date_created': datetime.utcnow()
    }
    
    return application_json, None

@app.route('/add-application', methods=['POST'])
def add_application():
    data = request.get_json()
    application_json, error = validate_and_create_application_json(data)

    if error:
        return jsonify({"success": False, "message": error}), 400

    try:
        result = applications_collection.insert_one(application_json)
        return jsonify({"success": True, "message": "Application added", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/update-application-status', methods=['POST'])
def update_application_status():
    data = request.get_json()
    application_id = data.get('application_id')
    new_status = data.get('status')

    # Validate application ID and status
    if not application_id:
        return jsonify({"success": False, "message": "Missing application_id"}), 400
    if new_status not in allowed_application_status:
        return jsonify({"success": False, "message": "Invalid status. Allowed statuses are: " + ", ".join(allowed_application_status)}), 400

    try:
        # Update the status of the application
        result = applications_collection.update_one(
            {"_id": ObjectId(application_id)}, 
            {"$set": {"status": new_status}}
        )
        if result.matched_count:
            return jsonify({"success": True, "message": "Application status updated"}), 200
        else:
            return jsonify({"success": False, "message": "Application not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
@app.route('/delete-application', methods=['DELETE'])
def delete_application():
    application_id = request.args.get('application_id')

    # Validate input
    if not application_id:
        return jsonify({"success": False, "message": "Missing application_id"}), 400

    try:
        # Delete the application
        result = applications_collection.delete_one({"_id": ObjectId(application_id)})
        if result.deleted_count:
            return jsonify({"success": True, "message": "Application deleted"}), 200
        else:
            return jsonify({"success": False, "message": "Application not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
