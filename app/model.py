from dataclasses import dataclass
from typing import List, Callable, Any, TypeVar, Type, cast

from app.network import Ship

T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Result:
    starships: List[Ship]
    starships_unknown_hyperdrive: List[Ship]

    def __int__(self, starships, starships_unknown_hyperdrive):
        self.starships = starships
        self.starships_unknown_hyperdrive = starships_unknown_hyperdrive

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        starships = from_list(Ship.from_dict, obj.get("starships"))
        starships_unknown_hyperdrive = from_list(Ship.from_dict, obj.get("starships_unknown_hyperdrive"))
        return Result(starships, starships_unknown_hyperdrive)

    def to_dict(self) -> dict:
        result: dict = { "starships": from_list(lambda x: to_class(Ship, x), self.starships),
                         "starships_unknown_hyperdrive": from_list(lambda x: to_class(Ship, x), self.starships_unknown_hyperdrive)}
        return result
