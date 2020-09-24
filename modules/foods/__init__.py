from flask import Blueprint

foods = Blueprint('foods', __name__)

from . import views
