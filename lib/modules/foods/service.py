import json
from logging import getLogger, DEBUG

from sqlalchemy.orm import joinedload

from lib.core.models import Food, Nutrient
from modules.foods.request import Request

from sqlalchemy import (
    func,
    and_,
    or_,
)

operations = {
    "Equal": lambda a, b: a == b,
    "Greater Than": lambda a, b: a > b,
    "Less Than": lambda a, b: a < b,
}


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
        if filters:
            for f in filters:
                query = FoodsService._apply_filter(query, f)
        return query

    @staticmethod
    def _apply_filter(query, the_filter):
        for f in query.all():
            Nutrient
        operations[the_filter.operator]
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
