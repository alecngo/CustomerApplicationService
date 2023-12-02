from flask import request
from .utils import MongoAPI

class AnimalsMongoAPI(MongoAPI):
    def __init__(self):
        super().__init__('animals')  # Initialize superclass with the 'animals' collection
        self.required_fields = ['animal_id', 'rescue_center', 'breed', 'image_url', 'adoptable']
        self.create_index('animal_id', unique=True)

    def post(self):
        data = request.get_json()
        return super().post(data)

    def get(self, animal_id=None):
        if animal_id:
            return super().get(animal_id)
        animal_id = request.args.get('_id')
        return super().get(animal_id)
    
    def put(self):
        data = request.get_json()
        return super().put(data)
    
    def delete(self):
        animal_id = request.args.get('_id')
        return super().delete(animal_id)