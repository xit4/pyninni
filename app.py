from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.nutrient import Nutrient, Nutrients
from resources.food import Food, Foods
from models.nutrient import NutrientModel
from models.food import FoodModel

app = Flask(__name__)
cors = CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "super.secret.key"

api = Api(app)


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


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Nutrient, '/nutrient/<int:nutrient_id>')
api.add_resource(Nutrients, '/nutrients')
api.add_resource(Food, '/food/<int:food_id>')
api.add_resource(Foods, '/foods')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
