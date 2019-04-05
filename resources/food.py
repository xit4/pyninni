from flask_restful import Resource, reqparse
from models.food import FoodModel
from flask_jwt_extended import (
    jwt_required,
)
import constants.strings as strings


class Food(Resource):
    @staticmethod
    @jwt_required
    def get(food_id):
        food = FoodModel.find_by_id(food_id)
        if not food:
            return {'message': strings.error_food_not_found}, 404
        return food.json(), 200


class Foods(Resource):
    @staticmethod
    @jwt_required
    def get():
        foods = FoodModel.get_all()
        if not foods:
            return {'message': strings.error_foods_not_found}, 404
        return {'items': [food.json() for food in FoodModel.query.all()]}, 200
