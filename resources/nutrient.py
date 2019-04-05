from flask_restful import Resource, reqparse
from models.nutrient import NutrientModel
from flask_jwt_extended import (
    jwt_required,
)
import constants.strings as strings


class Nutrient(Resource):
    @staticmethod
    @jwt_required
    def get(nutrient_id):
        nutrient = NutrientModel.find_by_id(nutrient_id)
        if not nutrient:
            return {'message': strings.error_nutrient_not_found}, 404
        return nutrient.json(), 200


class Nutrients(Resource):
    @staticmethod
    @jwt_required
    def get():
        nutrients = NutrientModel.get_all()
        if not nutrients:
            return {'message': strings.error_nutrients_not_found}, 404
        return {'items': [nutrient.json() for nutrient in NutrientModel.query.all()]}, 200
