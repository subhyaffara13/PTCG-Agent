
def statically_known_false(x: BoolLikeType) -> bool:
    """
    Returns True if x can be simplified to a constant and is False.
    If x cannot be evaluated from static, we return False

    .. note::
        This function doesn't introduce new guards, so the expression may end
        up evaluating to False at runtime even if this function returns False.

    Args:
        x (bool, SymBool): The expression to try statically evaluating
    """
    if not isinstance(x, SymBool):
        if not isinstance(x, bool):
            raise AssertionError(f"Expected bool, got {type(x)}")
        return not x

    result = _static_eval_sym_bool(x)
    if result is None:
        return False

    return not result

