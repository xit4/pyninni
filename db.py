from flask_sqlalchemy import SQLAlchemy
from models.nutrient import NutrientModel
from models.food import FoodModel

db = SQLAlchemy()


def init_db():
    print("Checking if Nutrients are initialized")
    nutrients = NutrientModel.query.all()
    if not nutrients:
        print("Initializing Nutrients")
        NutrientModel.initialize_nutrients()
    print("Checking if Foods are initialized")
    foods = FoodModel.query.all()
    if not foods:
        print("Initializing Foods")
        FoodModel.initialize_foods()
