
def is_concrete_float(a: FloatLikeType) -> bool:
    r"""Utility to check if underlying object
    in SymInt is concrete value. Also returns
    true if integer is passed in.

    Args:
        a (SymInt or float): Object to test if it float
    """
    if not isinstance(a, (SymFloat, float)):
        raise AssertionError(f"Expected SymFloat or float, got {type(a)}")

    if isinstance(a, float):
        return True

    if isinstance(a.node.expr, sympy.core.numbers.Float):
        return True

    return False

