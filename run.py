from app import app
from db import db, init_db
from models.nutrient import NutrientModel
from models.food import FoodModel

db.init_app(app)


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


@app.before_first_request
def create_tables():
    print("Creating DB")
    db.create_all()
    print("Initializing DB")
    init_db()
