
def _constrain_range_for_size(
    a: SymInt, min: int | None = None, max: int | None = None
) -> None:
    """
    This function is NOT INTENDED to be used by itself.
    """

    if isinstance(a, (SymFloat, SymBool)):
        raise ValueError("Constraining SymFloat/SymBool is nyi")

    if not isinstance(a, SymInt):
        raise AssertionError("can only constrain range for SymInt")
    if not isinstance(a.node.expr, sympy.Symbol):
        raise AssertionError(f"constraining non-Symbols NYI: {a}")

    a.node.shape_env._constrain_range_for_size(a.node.expr, min, max)

