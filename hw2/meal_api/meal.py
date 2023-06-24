from dish import Dish
from db import db


class Meal(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    appetizer = db.Column(db.Integer, db.ForeignKey("dish.id"), nullable=True)
    main = db.Column(db.Integer, db.ForeignKey("dish.id"), nullable=True)
    dessert = db.Column(db.Integer, db.ForeignKey("dish.id"), nullable=True)

    def to_dict(self):

        appetizer = Dish.query.filter_by(id=self.appetizer).first()
        main = Dish.query.filter_by(id=self.main).first()
        dessert = Dish.query.filter_by(id=self.dessert).first()
        serv = list(filter(lambda x: x is not None, [appetizer, main, dessert]))

        cal = sum(dish.cal for dish in serv)
        sodium = sum(dish.sodium for dish in serv)
        sugar = sum(dish.sugar for dish in serv)

        return {
            "name": self.name,
            "ID": self.id,
            "appetizer": appetizer.id if appetizer is not None else None,
            "main": main.id if main is not None else None,
            "dessert": dessert.id if dessert is not None else None,
            "cal": cal,
            "sodium": sodium,
            "sugar": sugar,
        }
