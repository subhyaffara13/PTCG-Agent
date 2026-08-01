
def is_trivial_suffix(param: Parameters | NormalizedCallableType) -> bool:
    param_star = param.var_arg()
    param_star2 = param.kw_arg()
    return (
        param.arg_kinds[-2:] == [ARG_STAR, ARG_STAR2]
        and param_star is not None
        and isinstance(get_proper_type(param_star.typ), AnyType)
        and param_star2 is not None
        and isinstance(get_proper_type(param_star2.typ), AnyType)
    )

