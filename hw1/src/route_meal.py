import os
from flask import Blueprint, request, abort
import requests
import urllib.parse

from meal import Meal
from dish import Dish
from db import db
from route_dish import get_dish
from flask import current_app

meal_blueprint = Blueprint("meal_blueprint", __name__)


@meal_blueprint.route("/meals", methods=["POST"])
def add_meal():
    """ """

    if request.content_type != "application/json":
        return "0", 415

    if not request.json:
        return "-1", 422

    if any(x not in request.json for x in ["appetizer", "main", "dessert", "name"]):
        return "-1", 422

    if (
        not isinstance(request.json["appetizer"], int)
        or not isinstance(request.json["main"], int)
        or not isinstance(request.json["dessert"], int)
    ):
        return "-1", 422

    appetizer = request.json["appetizer"]
    main = request.json["main"]
    dessert = request.json["dessert"]
    name = request.json["name"]
    if Meal.query.filter_by(name=name).first() is not None:
        return "-2", 422

    appetizer = get_dish(request.json["appetizer"])
    main = get_dish(request.json["main"])
    dessert = get_dish(request.json["dessert"])
    if any(x is None for x in [appetizer, main, dessert]):
        return "-6", 422
    meal = Meal(name=name, appetizer=appetizer.id, main=main.id, dessert=dessert.id)
    db.session.add(meal)
    db.session.commit()

    return str(meal.id), 201


@meal_blueprint.route("/meals", methods=["GET"])
def get_meals_list():
    """ """
    res = Meal.query
    return {meal.id:meal.to_dict() for meal in res.all()}


def get_meal(meal_id_or_name):
    if meal_id_or_name.isdigit():
        return Meal.query.filter_by(id=meal_id_or_name).first()
    return Meal.query.filter_by(name=meal_id_or_name).first()


@meal_blueprint.route("/meals/<meal_id_or_name>", methods=["GET"])
def get_meal_route(meal_id_or_name):
    """
    get dish id or name and return the dish details by looking for the dish id
    if dish name is given, look for its id in the dishes dict
    :param dish_id_or_name: dish id or dish name
    :return:
    """
    meal = get_meal(meal_id_or_name)
    return ("-5", 404) if meal is None else meal.to_dict()


@meal_blueprint.route("/meals/<meal_id_or_name>", methods=["DELETE"])
def delete_meal(meal_id_or_name):
    """ """
    meal = get_meal(meal_id_or_name)

    if meal is None:
        return "-5", 404

    meal_id = meal.id
    db.session.delete(meal)
    db.session.commit()
    return str(meal_id)


@meal_blueprint.route("/meals/<int:meal_id>", methods=["PUT"])
def put_meal(meal_id):
    if request.content_type != "application/json":
        return "0", 415

    if not request.json:
        return "-1", 422

    if any(x not in request.json for x in ["appetizer", "main", "dessert", "name"]):
        return "-1", 422

    if (
        not isinstance(request.json["appetizer"], int)
        or not isinstance(request.json["main"], int)
        or not isinstance(request.json["dessert"], int)
    ):
        return "-1", 422

    meal = Meal.query.filter_by(id=meal_id)
    if meal.first() is None:
        return "-5", 404

    appetizer = get_dish(request.json["appetizer"])
    main = get_dish(request.json["main"])
    dessert = get_dish(request.json["dessert"])
    if any(x is None for x in [appetizer, main, dessert]):
        return "-6", 422

    name = request.json["name"]

    if (
        Meal.query.filter_by(name=name).first() is not None
        and Meal.query.filter_by(name=name).first().id != meal_id
    ):
        return "-2", 422

    meal.update(
        dict(appetizer=appetizer.id, main=main.id, dessert=dessert.id, name=name)
    )
    db.session.commit()

    return str(meal_id)
