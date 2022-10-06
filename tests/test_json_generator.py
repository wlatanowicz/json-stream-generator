import json

import pytest

from json_stream_generator import json_generator


# fmt: off
@pytest.mark.parametrize(
    "depth",
    list(range(1, 6))
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
        (1, {"a": "b"}, ['{', '"a": ', '"b"', '}']),
        (2, {"a": "b"}, ['{', '"a": ', '"b"', '}']),
        (3, {"a": "b"}, ['{', '"a": ', '"b"', '}']),
        (1, {"a": [1,2,3]}, ['{', '"a": ', '[1, 2, 3]', '}']),
        (2, {"a": [1,2,3]}, ['{', '"a": ', '[', '1', ', ', '2', ', ', '3', ']', '}']),
    ]
)
# fmt: on
def test_output_in_chunks(depth, obj, expected):
    result = list(json_generator(obj, depth=depth))

    assert expected == result


def test_generator_input():
    obj = (num for num in range(5))
    # fmt: off
    expected = ["[", "0", ", ", "1", ", ", "2", ", ", "3", ", ", "4", "]"]
    # fmt: on

    result = list(json_generator(obj))

    assert expected == result
