from flask import Blueprint, request, abort

from db import db
from diet import Diet


diet_blueprint = Blueprint("diet_blueprint", __name__)


@diet_blueprint.route("/diets", methods=["POST"])
def add_dish():
    """
    :param dish_name:
    :return:
    """

    if request.content_type != "application/json":
        return "0", 415

    if not request.json or "name" not in request.json:
        return "-1", 422

    diet_name = request.json["name"]
    diet_cal = request.json.get("cal", None)
    diet_sodium = request.json.get("sodium", None)
    diet_sugar = request.json.get("sugar", None)

    if Diet.query.filter_by(name=diet_name).first() is not None:
        return f"Diet with {diet_name} already exists", 422
    try:
        diet = Diet(name=diet_name, cal=diet_cal, sodium=diet_sodium, sugar=diet_sugar)
        db.session.add(diet)
        db.session.commit()

    except ValueError:
        return "-3", 422

    except Exception as e:
        print(e)
        return e, 504

    return f"Diet {diet_name} was created successfully", 201


@diet_blueprint.route("/diets", methods=["GET"])
def get_dishes_list():
    """

    :param dish_name:
    :return:
    """
    res = Diet.query
    for val in request.args:
        res = (
            res.filter(getattr(Diet, val) <= request.args[val])
            if val in ["cal", "sodium", "sugar"]
            else res
        )
    return [dish.to_dict() for dish in res.all()]


@diet_blueprint.route("/diets/<diet_name>", methods=["GET"])
def get_dish_route(diet_name):
    """
    get dish id or name and return the dish details by looking for the dish id
    if dish name is given, look for its id in the dishes dict
    :param dish_id_or_name: dish id or dish name
    :return:
    """
    diet = Diet.query.filter_by(name=diet_name).first()
    return (f"Diet {diet_name} not found", 404) if diet is None else diet.to_dict()


@diet_blueprint.route("/diets/<diet_name>", methods=["DELETE"])
def delete_dish(diet_name):
    """
    delete dish id or name and return the deleted dish id
    if dish name is given, look for its id in the dishes dict
    :param dish_id_or_name: dish id or dish name
    :return: dish id of the deleted dish
    """

    diet = Diet.query.filter_by(name=diet_name).first()
    if diet is None:
        return f"Diet {diet_name} not found", 404
    db.session.delete(diet)
    db.session.commit()
    return f"Diet {diet_name} deleted successfully", 200
