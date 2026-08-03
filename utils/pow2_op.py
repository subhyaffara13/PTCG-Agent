from typing import Any

def pow2_op(data: Any, dim: str, exponent: int) -> bool:
    return data[dim] == 2**exponent

