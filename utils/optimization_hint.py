
def optimization_hint(a: torch.SymInt | int, fallback: int | None = None) -> int:
    """
    Return a concrete hint for a symbolic integer, for use in optimization decisions.

    Unlike guarding_hint_or_throw, this function does not add guards and is intended
    for optimization purposes only (e.g., memory estimation).
    """
    if isinstance(a, torch.SymInt):
        if a.node._hint is not None:
            return a.node._hint
        return a.node.shape_env.optimization_hint(a.node.expr, fallback=fallback)
    if type(a) is not int:
        raise AssertionError(f"Expected int, got {type(a)}")
    return a

