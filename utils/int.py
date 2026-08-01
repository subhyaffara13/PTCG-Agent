
def int(value: builtins.int) -> bool:
    r"""Signed 64-bit integer (:math:`-2^{63} \leq x < 2^{63}`)"""
    return -(2**63) <= value < 2**63

