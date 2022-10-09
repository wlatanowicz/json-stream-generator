import json
from datetime import datetime

import pytest

from json_stream_generator import json_generator


# fmt: off
@pytest.mark.parametrize(
    "depth",
    list(range(0, 4))
)
@pytest.mark.parametrize(
    "obj",
    (
        {"a": "b"},
        ["a", "b", "c", "d"],
        {"a": "b", "c": "d"},
        {"a": "b", "c": []},
        {"a": "b", "c": [1, 2, 3]},
        {"a": "b", "c": [1, "a", {"a": "b", "c": 2}]},
        "abcd",
        234,
        {},
        [],
        {"a": []},
        {"a": {}},
        [{}],
        [[]],
        [{}, []],
        [[], []],
        {"a": [{}, {}]},
    )
)
# fmt: on
def test_output_equals_json_dumps(depth, obj):
    expected = json.dumps(obj)
    result = "".join(json_generator(obj, depth=depth))

    assert expected == result


# fmt: off
@pytest.mark.parametrize(
    "depth, obj, expected",
    [
        (0, {"a": "b"}, ['{"a": "b"}']),
        (1, {"a": "b"}, ['{"a": ', '"b"', '}']),
        (2, {"a": "b"}, ['{"a": ', '"b"', '}']),
        (3, {"a": "b"}, ['{"a": ', '"b"', '}']),
        (1, {"a": [1,2,3]}, ['{"a": ', '[1, 2, 3]', '}']),
        (2, {"a": [1,2,3]}, ['{"a": ', '[1', ', 2', ', 3', ']', '}']),
    ]
)
# fmt: on
def test_output_in_chunks(depth, obj, expected):
    result = list(json_generator(obj, depth=depth))

    assert expected == result


def test_generator_input():
    obj = (num for num in range(5))
    # fmt: off
    expected = ["[0", ", 1", ", 2", ", 3", ", 4", "]"]
    # fmt: on

    result = list(json_generator(obj))

    assert expected == result


def test_simple_values():
    obj = [
        {},
        [],
        (),
        123,
        123.456,
        True,
        False,
        None,
        "abc",
    ]
    expected = json.dumps(obj)
    result = "".join(json_generator(obj))

    assert expected == result


def test_different_key_types():
    obj = {
        123: "A",
        123.456: "B",
        True: "C",
        False: "D",
        None: "E",
        "abc": "F",
    }
    expected = json.dumps(obj)
    result = "".join(json_generator(obj))

    assert expected == result


# fmt: off
@pytest.mark.parametrize(
    "obj",
    [
        {(1, 2): "A"},
        [{(1, 2): "A"}],
        {datetime.now(): "A"},
        [{datetime.now(): "A"}],
        ({datetime.now(): "A"} for _ in range(5)),
        ({(1, 2): "A"} for _ in range(5)),
    ]
)
# fmt: on
def test_invalid_keys(obj):
    with pytest.raises(TypeError):
        "".join(json_generator(obj))
