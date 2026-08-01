
def validate_func(fname, args, kwargs) -> None:
    if fname not in _validation_funcs:
        return validate_stat_func(args, kwargs, fname=fname)

    validation_func = _validation_funcs[fname]
    return validation_func(args, kwargs)

