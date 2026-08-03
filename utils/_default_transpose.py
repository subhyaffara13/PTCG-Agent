from typing import Tuple

def _default_transpose(x: ArrayType, axes: Tuple[int, ...]) -> ArrayType:
    #  most libraries implement a method version
    return x.transpose(axes)

