
def any_dims(func, *args, **kwargs):
    return _apply_reduction(func, "any", False, *args, **kwargs)

