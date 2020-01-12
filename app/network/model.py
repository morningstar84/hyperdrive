# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = star_ships_list_from_dict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, TypeVar, Callable, Type, cast, Optional

import dateutil.parser

T = TypeVar("T")


def from_float(x: Any) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


def from_str(x: Any) -> str:
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Ship:
    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    hyperdrive_rating: float
    mglt: str
    starship_class: str
    pilots: List[str]
    films: List[str]
    created: datetime
    edited: datetime
    url: str

    @property
    def has_hyperdrive_rating(self):
        return self.hyperdrive_rating is not None

    @staticmethod
    def from_dict(obj: Any) -> 'Ship':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        model = from_str(obj.get("model"))
        manufacturer = from_str(obj.get("manufacturer"))
        cost_in_credits = from_str(obj.get("cost_in_credits"))
        length = from_str(obj.get("length"))
        max_atmosphering_speed = from_str(obj.get("max_atmosphering_speed"))
        crew = from_str(obj.get("crew"))
        passengers = from_str(obj.get("passengers"))
        cargo_capacity = from_str(obj.get("cargo_capacity"))
        consumables = from_str(obj.get("consumables"))
        hyperdrive_rating = from_float(obj.get("hyperdrive_rating"))
        mglt = from_str(obj.get("MGLT"))
        starship_class = from_str(obj.get("starship_class"))
        pilots = from_list(from_str, obj.get("pilots"))
        films = from_list(from_str, obj.get("films"))
        created = from_datetime(obj.get("created"))
        edited = from_datetime(obj.get("edited"))
        url = from_str(obj.get("url"))
        return Ship(name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, mglt, starship_class, pilots, films, created, edited, url)

    def to_dict(self) -> dict:
        result: dict = {"name": from_str(self.name)}
        if self.has_hyperdrive_rating:
            result["hyperdrive_rating"] = from_float(self.hyperdrive_rating)
        return result


@dataclass
class StarShipsList:
    count: int
    next: str
    previous: str
    results: List[Ship]

    @staticmethod
    def from_dict(obj: Any) -> 'StarShipsList':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        next = from_str(obj.get("next"))
        previous = from_str(obj.get("previous"))
        results = from_list(Ship.from_dict, obj.get("results"))
        return StarShipsList(count, next, previous, results)

    def to_dict(self) -> dict:
        result: dict = {"count": from_int(self.count), "next": from_str(self.next), "previous": from_str(self.previous),
                        "results": from_list(lambda x: to_class(Ship, x), self.results)}
        return result


def star_ships_list_from_dict(s: Any) -> StarShipsList:
    return StarShipsList.from_dict(s)


def star_ships_list_to_dict(x: StarShipsList) -> Any:
    return to_class(StarShipsList, x)
