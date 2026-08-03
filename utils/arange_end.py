from typing import Any
import math


def arange_end(end: number, inp0: Any, inp1: Any, inp2: Any, inp3: Any):
    if end < 0:
        raise AssertionError(f"Expected end ({end}) >= 0")
    return [int(math.ceil(end))]

