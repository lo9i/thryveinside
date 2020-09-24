from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from typing import List, Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Nutrient:
    nutrient_id: str
    nutrient: str
    unit: str
    value: str
    gm: str


@dataclass_json(letter_case=LetterCase.CAMEL)
class Food:
    ndbno: str
    name: str
    weight: float
    measure: str
    nutrients: Optional[List[Nutrient]] = None
