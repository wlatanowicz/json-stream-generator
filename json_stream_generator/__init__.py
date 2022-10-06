import inspect
import json
from os import path
from typing import Any, Generator

with open(path.join(path.dirname(__file__), "VERSION")) as f:
    __version__ = f.read().strip()

__author__ = "Wiktor Latanowicz"


def json_generator(obj: Any, depth: int = 1) -> Generator[str, None, None]:
    if depth < 1:
        yield json.dumps(obj)
    elif isinstance(obj, dict):
        yield "{"
        for i, (key, value) in enumerate(obj.items()):
            if i > 0:
                yield ", "
            yield json.dumps(str(key)) + ": "
            yield from json_generator(value, depth=depth - 1)
        yield "}"
    elif isinstance(obj, (list, tuple)) or inspect.isgenerator(obj):
        yield "["
        for i, item in enumerate(obj):
            if i > 0:
                yield ", "
            yield from json_generator(item, depth=depth - 1)
        yield "]"
    else:
        yield json.dumps(obj)
