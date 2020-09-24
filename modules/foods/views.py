
from flask import request, abort, jsonify
from flask_cors import cross_origin

from app import app
from lib import FoodsService
from . import foods


@foods.route("/", methods=["POST", "OPTIONS"])
@cross_origin(
    allow_headers=["Content-Type", "Authorization"],
    origins=app.config["CORS_ORIGINS"],
    supports_credentials=True,
)
def list():
    try:
        response = foods_service.get_foods(request.data)
        return jsonify(response)
    except KeyError:
        abort(400)


@foods.route("/<int:food_id>", methods=["GET"])
@cross_origin(
    allow_headers=["Content-Type", "Authorization"],
    origins=app.config["CORS_ORIGINS"],
    supports_credentials=True,
)
def get(food_id):
    try:
        response = foods_service.get_food(food_id)
        return jsonify(response)
    except KeyError:
        abort(400)


foods_service = FoodsService()
