import json

from app import db, app
from lib.core.models import Food, Nutrient, FoodNutrient


def add_nutrients(data):
    nutrients = {}
    for f in data['foods']:
        for n in f['nutrients']:
            nutrients[n['nutrient']] = n

    for n in nutrients.values():
        nutrient = Nutrient()
        nutrient.id = n['nutrient_id']
        nutrient.name = n['nutrient']
        nutrient.unit = n['unit']
        nutrient.value = n['value']
        nutrient.gm = n['gm']
        db.session.add(nutrient)
        db.session.commit()


def add_foods(data):
    for f in data['foods']:
        food = Food()
        food.name = f['name']
        food.weight = f['weight']
        food.measure = f['measure']
        db.session.add(food)
        db.session.commit()

        for n in f['nutrients']:
            food_nutrient = FoodNutrient()
            food_nutrient.food_id = food.id
            food_nutrient.nutrient_id = n['nutrient_id']
            db.session.add(food_nutrient)
            db.session.commit()


with open('dbs/food_data.json') as f:
    data = json.load(f)
    with app.app_context():
        add_nutrients(data)
        add_foods(data)
