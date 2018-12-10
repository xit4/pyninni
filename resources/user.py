import sqlite3
import datetime
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required, get_jwt_claims,
    get_jwt_identity
)
import constants.strings as strings


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help=strings.error_user_required
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help=strings.error_password_required
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help=strings.error_email_required
                        )
    parser.add_argument('first_name',
                        type=str,
                        )
    parser.add_argument('last_name',
                        type=str,
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": strings.error_username_not_unique}, 400

        if UserModel.find_by_email(data['email']):
            return {"message": strings.error_email_not_unique}, 400

        now = datetime.datetime.now()
        user = UserModel(**data, creation_date=now)
        try:
            user.save_to_db()
        except BaseException as e:
            print(e)
            return {'message': strings.error_user_generic}, 500

        return {"message": strings.success_user_created}, 201


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)

    @staticmethod
    @jwt_required
    def get(user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': strings.error_user_not_found}, 404
        return user.json()

    @staticmethod
    @jwt_required
    def delete(user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': strings.error_not_admin}, 403
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': strings.error_user_not_found}, 404
        user.delete_from_db()
        return {'message': strings.success_user_deleted}, 200

    @staticmethod
    @jwt_required
    def patch(user_id):
        claims = get_jwt_claims()
        current_user_id = get_jwt_identity()
        if current_user_id != user_id and not claims['is_admin']:
            return {'message': strings.error_patch_other}, 403
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': strings.error_user_not_found}, 404

        data = User.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": strings.error_username_not_unique}, 400
        if UserModel.find_by_email(data['email']):
            return {"message": strings.error_email_not_unique}, 400
        print(data)
        return {'message': "wow"}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="The username cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="The password cannot be left blank!"
                        )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200

        return {
            "message": "Invalid credentials"
        }, 401


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(
            identity=current_user_id, fresh=False)
        return {
            'access_token': new_access_token,
        }, 200
