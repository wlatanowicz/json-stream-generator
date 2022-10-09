import inspect
import json
from os import path
from typing import Any, Generator

with open(path.join(path.dirname(__file__), "VERSION")) as f:
    __version__ = f.read().strip()

__author__ = "Wiktor Latanowicz"


KEY_CONVERSION_LUT = {
    None: "null",
    True: "true",
    False: "false",
}


def json_generator(obj: Any, depth: int = 1) -> Generator[str, None, None]:
    if depth < 1:
        yield json.dumps(obj)
    elif isinstance(obj, dict):
        not_first = False
        for key, value in obj.items():
            prefix = ", " if not_first else "{"
            if not isinstance(key, (str, int, float, bool)) and key is not None:
                raise TypeError(
                    f"keys must be str, int, float, bool or None, not {key.__class__.__name__}"
                )

            yield prefix + json.dumps(str(KEY_CONVERSION_LUT.get(key, key))) + ": "
            yield from json_generator(value, depth=depth - 1)
            not_first = True
        yield "}" if not_first else "{}"
    elif isinstance(obj, (list, tuple)) or inspect.isgenerator(obj):
        not_first = False
        for item in obj:
            prefix = ", " if not_first else "["
            for j, item in enumerate(json_generator(item, depth=depth - 1)):
                yield item if j > 0 else prefix + item
            not_first = True
        yield "]" if not_first else "[]"
    else:
        yield json.dumps(obj)
