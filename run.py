from flask import Flask, jsonify
from flask_restful import Api
import os
from app import app

from app.views import add_customer, find_customer

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")

    app.run(host='0.0.0.0', port=8001)