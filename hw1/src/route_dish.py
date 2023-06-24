from flask import Blueprint, request, abort

from db import db
from dish import Dish


dish_blueprint = Blueprint("dish_blueprint", __name__)


@dish_blueprint.route("/dishes", methods=["POST"])
def add_dish():
    """
    :param dish_name:
    :return:
    """

    if request.content_type != "application/json":
        return "0", 415

    if not request.json or "name" not in request.json:
        return "-1", 422

    dish_name = request.json["name"]

    if Dish.query.filter_by(name=dish_name).first() is not None:
        return "-2", 422
    try:
        dish = Dish(dish_name)
        db.session.add(dish)
        db.session.commit()

    except ValueError:
        return "-3", 422

    except Exception as e:
        print(e)
        return "-4", 504

    return str(dish.id), 201


@dish_blueprint.route("/dishes", methods=["GET"])
def get_dishs_list():
    """

    :param dish_name:
    :return:
    """
    res = Dish.query
    for val in request.args:
        res = (
            res.filter(getattr(Dish, val) <= request.args[val])
            if val in ["cal", "sodium", "sugar"]
            else res
        )
    return {dish.id :dish.to_dict() for dish in res.all()}


def get_dish(dish_id_or_name):
    if str(dish_id_or_name).isdigit():
        return Dish.query.filter_by(id=dish_id_or_name).first()
    return Dish.query.filter_by(name=dish_id_or_name).first()


@dish_blueprint.route("/dishes/<dish_id_or_name>", methods=["GET"])
def get_dish_route(dish_id_or_name):
    """
    get dish id or name and return the dish details by looking for the dish id
    if dish name is given, look for its id in the dishes dict
    :param dish_id_or_name: dish id or dish name
    :return:
    """
    print("~"*30,dish_id_or_name)
    dish = get_dish(dish_id_or_name)
    return ("-5", 404) if dish is None else dish.to_dict()


@dish_blueprint.route("/dishes/<dish_id_or_name>", methods=["DELETE"])
def delete_dish(dish_id_or_name):
    """
    delete dish id or name and return the deleted dish id
    if dish name is given, look for its id in the dishes dict
    :param dish_id_or_name: dish id or dish name
    :return: dish id of the deleted dish
    """
    dish = get_dish(dish_id_or_name)
    if dish is None:
        return "-5", 404
    dish_id = dish.id
    db.session.delete(dish)
    db.session.commit()
    return str(dish_id)
