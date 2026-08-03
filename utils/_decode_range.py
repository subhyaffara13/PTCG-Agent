from typing import Tuple

def _decode_range(r: int) -> tuple[int, int]:
    return (r >> 32), (r & ((1 << 32) - 1))


def _decode_range(r: int) -> Tuple[int, int]:
    return (r >> 32), (r & ((1 << 32) - 1))

