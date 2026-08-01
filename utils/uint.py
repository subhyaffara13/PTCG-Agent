
def uint(value: builtins.int) -> bool:
    r"""Unsigned 64-bit integer (:math:`0 \leq x < 2^{64}`)"""
    return 0 <= value < 2**64

