import requests
import os
from db import db


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    cal = db.Column(db.Float, nullable=False)
    size = db.Column(db.Float, nullable=False)
    sodium = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)

    def __init__(self, name):
        """

        :param name: dish name
        """
        self.name = name
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query={self.name}"
        response = requests.get(
            api_url, headers={"X-Api-Key": os.environ.get("API_KEY")}
        )

        if len(response.json()) == 0:
            raise ValueError("No such dish")
        super().__init__(
            name=name,
            cal=sum(dish["calories"] for dish in response.json()),
            size=sum(dish["serving_size_g"] for dish in response.json()),
            sodium=sum(dish["sodium_mg"] for dish in response.json()),
            sugar=sum(dish["sugar_g"] for dish in response.json()),
        )

    def to_dict(self):
        return {
            "name": self.name,
            "cal": self.cal,
            "sodium": self.sodium,
            "sugar": self.sugar,
            "size": self.size,
            "ID": self.id,
        }
