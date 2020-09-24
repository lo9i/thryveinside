from dataclasses import dataclass, field
from typing import Optional, List

from sqlalchemy.orm import relationship, backref

from app import db


@dataclass
class Food(db.Model):
    __tablename__ = 'food'
    id: int
    name: str
    weight: float
    measure: str
    nutrients: Optional[List] = field(default_factory=list)

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    weight = db.Column('weight', db.Float)
    measure = db.Column('measure', db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


@dataclass
class Nutrient(db.Model):
    __tablename__ = 'nutrient'
    id: int
    name: str
    unit: str
    value: float
    gm: float

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), unique=True)
    unit = db.Column('unit', db.String(50), unique=True)
    value = db.Column('value', db.Float)
    gm = db.Column('gm', db.Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


@dataclass
class FoodNutrient(db.Model):
    __tablename__ = 'food_nutrient'
    id: int
    food_id: int
    nutrient_id: int

    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrient.id'))

    food = relationship(Food, backref=backref("nutrients", cascade="all, delete-orphan"))
    nutrient = relationship(Nutrient, backref=backref("foods", cascade="all, delete-orphan"))
