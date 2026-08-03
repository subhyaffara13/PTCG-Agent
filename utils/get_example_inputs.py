from typing import Any

def get_example_inputs(key: str) -> list[Any]:
    global _EXAMPLE_INPUTS
    if _EXAMPLE_INPUTS is None:
        _EXAMPLE_INPUTS = {}

    if key not in _EXAMPLE_INPUTS:
        _EXAMPLE_INPUTS[key] = []

    return _EXAMPLE_INPUTS[key]

