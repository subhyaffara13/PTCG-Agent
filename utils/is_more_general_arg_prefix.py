
def is_more_general_arg_prefix(t: FunctionLike, s: FunctionLike) -> bool:
    """Does t have wider arguments than s?"""
    # TODO should an overload with additional items be allowed to be more
    #      general than one with fewer items (or just one item)?
    if isinstance(t, CallableType):
        if isinstance(s, CallableType):
            return is_callable_compatible(
                t, s, is_compat=is_proper_subtype, is_proper_subtype=True, ignore_return=True
            )
    elif isinstance(t, FunctionLike):
        if isinstance(s, FunctionLike):
            if len(t.items) == len(s.items):
                return all(
                    is_same_arg_prefix(items, itemt) for items, itemt in zip(t.items, s.items)
                )
    return False

