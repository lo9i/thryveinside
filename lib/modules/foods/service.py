import json
from logging import getLogger, DEBUG

from sqlalchemy.orm import joinedload, load_only

from lib.core.models import Food, Nutrient, FoodNutrient
from modules.foods.request import Request

from sqlalchemy import (
    func,
    and_,
    or_,
)

logger = getLogger(__name__)


class FoodsService:

    _echo = False
    _tables = {}
    _schema = None

    def __init__(self):
        self._echo = logger.root.level == DEBUG

    def get_foods(self, request_str):
        '''
        Retrieves food that matches the filters
        :param filters:
        :return:
        '''

        logger.debug("Getting filtered food")
        request_dict = json.loads(request_str)
        request = Request.from_dict(request_dict)
        query = FoodsService._apply_filtering(request.filters)
        query, total_count = FoodsService._apply_paging(query, request.page)
        return {
            'results': query.all(),
            'count': total_count
        }

    def get_food(self, food_id):
        '''
        Retrieves food that matches the filters
        :param filters:
        :return:
        '''

        logger.debug("Getting filtered food")
        return Food.query.options(joinedload("nutrients")).filter(Food.id == food_id).first()

    def get_nutrients(self):
        return Nutrient.query.all()

    @staticmethod
    def _apply_filtering(filters):
        query = Food.query
        # some filters may be invalid
        if filters:
            filters = [f for f in filters if f.value is not None and f.value != '' and f.nutrient_id > 0]
        if filters:
            query = query.join(FoodNutrient, Food.nutrients)
            for f in filters:
                query = FoodsService._get_filter(query, f)
        return query

    @staticmethod
    def _get_filter(query, the_filter):
        if the_filter.operator == "Equal":
            return query.filter(and_(FoodNutrient.value != None, FoodNutrient.value == float(the_filter.value), FoodNutrient.nutrient_id == the_filter.nutrient_id))
        if the_filter.operator == "Greater Than":
            return query.filter(and_(FoodNutrient.value != None, FoodNutrient.value > float(the_filter.value), FoodNutrient.nutrient_id == the_filter.nutrient_id))
        if the_filter.operator == "Less Than":
            return query.filter(and_(FoodNutrient.value != None, FoodNutrient.value < float(the_filter.value), FoodNutrient.nutrient_id == the_filter.nutrient_id))
        logger.debug(f'Unknown filter type {the_filter.operator}')
        return query

    @staticmethod
    def _apply_paging(query, page):
        total_count = query.count()
        if page is not None:
            query_offset = page.index * page.size

            # Check if the requested page index is beyond the end
            # If so, then reset to first page.
            if total_count > query_offset:
                query = query.offset(query_offset).limit(page.size)
            else:
                page.index = 0

        return query, total_count
