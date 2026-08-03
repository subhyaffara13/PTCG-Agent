from typing import Any, Tuple

def test_get_shapes(array: Any, shape: Tuple[int]) -> None:
    assert get_shape(array) == shape

