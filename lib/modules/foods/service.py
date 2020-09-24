import json
import logging

from sqlalchemy.orm import joinedload

from lib.core.models import Food
from modules.foods.request import Request

logger = logging.getLogger(__name__)

from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    select,
    asc,
    desc,
    func, cast, Numeric
)
from logging import getLogger, DEBUG


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
        query = self._apply_filtering(request.filters)
        query, total_count = FoodsService._apply_paging(query, request.page)
        return {
            'results': query.all(),
            'count': total_count
        }
        # return json.dumps(result, cls=new_alchemy_encoder(), check_circular=False)

    def get_food(self, food_id):
        '''
        Retrieves food that matches the filters
        :param filters:
        :return:
        '''

        logger.debug("Getting filtered food")
        return Food.query.options(joinedload("nutrients")).filter(Food.id == food_id).first()
        # return json.dumps(result, cls=new_alchemy_encoder(), check_circular=False)

    def _apply_filtering(self, filters):
        if not filters:
            return Food.query

        # from lib import JsonService
        # sql_filters = JsonService.parse(table, filters)
        # return query.where(sql_filters)

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
