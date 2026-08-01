
def prod_dim_int(func, *args, **kwargs):
    return _apply_reduction(func, "prod", 1, *args, **kwargs)

