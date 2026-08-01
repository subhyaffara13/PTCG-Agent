
def all_dims(func, *args, **kwargs):
    return _apply_reduction(func, "all", True, *args, **kwargs)

