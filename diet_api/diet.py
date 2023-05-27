import requests
import os
from db import db


class Diet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    cal = db.Column(db.Float, nullable=True)
    sodium = db.Column(db.Float, nullable=True)
    sugar = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "name": self.name,
            "cal": self.cal,
            "sodium": self.sodium,
            "sugar": self.sugar,
        }
