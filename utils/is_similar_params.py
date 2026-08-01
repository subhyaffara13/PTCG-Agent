
def is_similar_params(t: Parameters, s: Parameters) -> bool:
    # This matches the logic in is_similar_callables() above.
    return (
        len(t.arg_types) == len(s.arg_types)
        and t.min_args == s.min_args
        and (t.var_arg() is not None) == (s.var_arg() is not None)
    )

