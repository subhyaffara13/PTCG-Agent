
def is_same_arg_prefix(t: CallableType, s: CallableType) -> bool:
    return is_callable_compatible(
        t,
        s,
        is_compat=is_same_type,
        is_proper_subtype=True,
        ignore_return=True,
        check_args_covariantly=True,
        ignore_pos_arg_names=True,
    )

