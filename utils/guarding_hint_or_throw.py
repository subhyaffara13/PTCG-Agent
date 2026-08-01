
def guarding_hint_or_throw(
    a: torch.SymInt | torch.SymBool | int | bool | SymNode,
) -> int | bool:
    """
    Return a concrete hint for a symbolic value, for use in guarding decisions.

    Returns Python bool (True/False) for boolean inputs (SymBool, bool),
    and Python int for integer inputs (SymInt, int).
    """
    if isinstance(a, SymNode):
        if a._hint is not None:
            return a._hint  # pyrefly: ignore[bad-return]
        if a.shape_env is None:
            raise AssertionError("shape_env is required for guarding_hint_or_throw")
        hint = a.shape_env.guarding_hint_or_throw(a.expr)
        a._hint = hint
        return hint
    if isinstance(a, (torch.SymInt, torch.SymBool)):
        return guarding_hint_or_throw(a.node)
    if isinstance(a, bool):
        return a
    if type(a) is not int:
        raise AssertionError(f"Expected int, got {type(a)}")
    return a

