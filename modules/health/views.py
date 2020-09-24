import os
from . import health


@health.route("/hz")
def hz():
    return "OK"


@health.route("/ready")
def ready():
    if os.path.exists("dbs/foods.db"):
        return "OK"
    return "Foods file doesn't exist", 400
