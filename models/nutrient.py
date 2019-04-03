from db import db
import json as jsonTools


class NutrientModel(db.Model):
    __tablename__ = "nutrients"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), unique=True)
    unit = db.Column(db.String(80))

    def __init__(self, label, unit):
        self.label = label
        self.unit = unit

    def json(self):
        return {
            "id": self.id,
            "label": self.label,
            "unit": self.unit,
        }

    @classmethod
    def find_by_label(cls, label):
        return cls.query.filter_by(label=label).first()

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
    def initialize_nutrients(cls):
        with open('./constants/nutrientsUnits.json') as f:
            nutrients = jsonTools.load(f)
            for i in range(len(nutrients)):
                nutrient = nutrients[str(i)]
                print("Adding nutrient {} with unit {}".format(
                    nutrient['label'], nutrient['unit']))
                db.session.add(NutrientModel(
                    nutrient['label'], nutrient['unit']))
        db.session.commit()
