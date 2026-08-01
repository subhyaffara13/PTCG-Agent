
def sum_dim_IntList(func, *args, **kwargs):
    return _apply_reduction(func, "sum", 0, *args, **kwargs)

