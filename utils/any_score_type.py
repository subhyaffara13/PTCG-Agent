
def any_score_type(ut: Type, arg_pos: bool) -> float:
    """Generate a very made up number representing the Anyness of a type.

    Higher is better, 1.0 is max
    """
    t = get_proper_type(ut)
    if isinstance(t, AnyType) and t.type_of_any != TypeOfAny.suggestion_engine:
        return 0
    if isinstance(t, NoneType) and arg_pos:
        return 0.5
    if isinstance(t, UnionType):
        if any(isinstance(get_proper_type(x), AnyType) for x in t.items):
            return 0.5
        if any(has_any_type(x) for x in t.items):
            return 0.25
    if isinstance(t, CallableType) and is_tricky_callable(t):
        return 0.5
    if has_any_type(t):
        return 0.5

    return 1.0

