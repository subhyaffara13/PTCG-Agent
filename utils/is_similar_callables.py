
def is_similar_callables(t: CallableType, s: CallableType) -> bool:
    """Return True if t and s have identical numbers of
    arguments, default arguments and varargs.
    """
    return (
        len(t.arg_types) == len(s.arg_types)
        and t.min_args == s.min_args
        and t.is_var_arg == s.is_var_arg
    )

