from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase

from typing import List, Dict, Optional


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Filter:
    id: int
    values: List = field(default_factory=lambda: [])


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Request:
    filters: Optional[List[Filter]] = field(default_factory=lambda: [])
