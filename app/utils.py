from flask.views import MethodView
from flask import jsonify, request
from bson import ObjectId
from .db import MongoSingleton
from pymongo.errors import DuplicateKeyError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoAPI(MethodView):

    def __init__(self, collection_name):
        self.mongo_instance = MongoSingleton()
        self.collection = self.mongo_instance.get_collection(collection_name)
        self.required_fields = []

    def convert_objectid_to_str(self, data):
        if isinstance(data, list):
            return [self.convert_objectid_to_str(item) for item in data]
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                else:
                    data[key] = self.convert_objectid_to_str(value)
        return data
    
    def create_index(self, field_name, unique=False):
        self.collection.create_index([(field_name, 1)], unique=unique)

    def validate_document(self, data):
        if not all(field in data for field in self.required_fields):
            missing_fields = [field for field in self.required_fields if field not in data]
            return f"Missing fields: {', '.join(missing_fields)}"
        return None

    def post(self, data):
        error = self.validate_document(data)
        if error:
            return jsonify({"success": False, "message": error}), 400
        try:
            result = self.collection.insert_one(data)
            inserted_document = self.collection.find_one({"_id": result.inserted_id})
            inserted_document = self.convert_objectid_to_str(inserted_document)
            return jsonify({"success": True, "message": "Document added", "data": inserted_document}), 201
        except DuplicateKeyError:
            return jsonify({"success": False, "message": "Document with given key already exists"}), 409
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    def get(self, document_id):
        logger.info("ID: %s", document_id)
        if not document_id:
            return jsonify({"error": "Missing _id parameter"}), 400

        try:
            query = {"_id": ObjectId(document_id)}
        except Exception:
            return jsonify({"error": "Invalid _id format"}), 400

        document = self.collection.find_one(query)
        if document:
            document = self.convert_objectid_to_str(document)
            return jsonify(document), 200
        else:
            return jsonify({"error": "Document not found"}), 404

    def put(self, data):
        document_id = data.pop('_id', None)
        if not document_id:
            return jsonify({"error": "Missing document ID"}), 400
        try:
            result = self.collection.update_one({"_id": ObjectId(document_id)}, {"$set": data})
            if result.modified_count:
                return jsonify({"success": True, "message": "Document updated"}), 200
            else:
                return jsonify({"error": "Document not found or no new data to update"}), 404
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

    def delete(self, document_id):
        if not document_id:
            return jsonify({"error": "Missing document ID"}), 400
        try:
            result = self.collection.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count:
                return jsonify({"success": True, "message": "Document deleted"}), 200
            else:
                return jsonify({"error": "Document not found"}), 404
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500

