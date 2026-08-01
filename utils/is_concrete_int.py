
def is_concrete_int(a: IntLikeType) -> bool:
    """
    Utility to check if underlying object
    in SymInt is concrete value. Also returns
    true if integer is passed in.

    Args:
        a (SymInt or int): Object to test if it int
    """
    if not isinstance(a, (SymInt, int)):
        raise AssertionError(f"Expected SymInt or int, got {type(a)}")

    if isinstance(a, int):
        return True

    if isinstance(a.node.expr, sympy.core.numbers.Integer):
        return True

    return False

