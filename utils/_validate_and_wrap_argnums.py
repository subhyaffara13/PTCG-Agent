
def _validate_and_wrap_argnums(argnums: argnums_t, num_args: int) -> argnums_t:
    if isinstance(argnums, int):
        return _validate_and_wrap_argnum(argnums, num_args)
    if isinstance(argnums, tuple):
        return tuple(_validate_and_wrap_argnum(argnum, num_args) for argnum in argnums)
    raise AssertionError("Should never get here")

