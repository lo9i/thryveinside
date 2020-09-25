from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

from typing import List, Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=False)
class Page:
    index: int
    size: Optional[int] = 25


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Filter:
    nutrient_id: int
    operator: str
    value: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Request:
    filters: Optional[List[List[Filter]]] = field(default_factory=lambda: [[]])
    page: Optional[Page] = None

