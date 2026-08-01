
def is_concrete_bool(a: BoolLikeType) -> bool:
    """
    Utility to check if underlying object
    in SymBool is concrete value. Also returns
    true if integer is passed in.

    Args:
        a (SymBool or bool): Object to test if it bool
    """
    if not isinstance(a, (SymBool, bool)):
        raise AssertionError(f"Expected SymBool or bool, got {type(a)}")

    if isinstance(a, bool):
        return True

    if isinstance(
        a.node.expr, (sympy.logic.boolalg.BooleanTrue, sympy.logic.boolalg.BooleanFalse)
    ):
        return True

    return False

