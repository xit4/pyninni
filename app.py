import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, User, UserLogin, TokenRefresh

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "super.secret.key"

api = Api(app)

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


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
