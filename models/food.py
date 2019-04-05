from db import db
import json as jsonTools


class FoodModel(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    nutrients = db.Column(db.JSON)

    def __init__(self, name, nutrients):
        self.name = name
        self.nutrients = nutrients

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "nutrients": self.nutrients,
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def initialize_foods(cls):
        with open('./constants/foodNutrientsObject.json') as f:
            foods = jsonTools.load(f)
            for i in range(len(foods)):
                food = foods[str(i)]
                db.session.add(FoodModel(
                    food['name'], food['nutrients']))
        db.session.commit()
