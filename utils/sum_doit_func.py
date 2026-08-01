
def sum_doit_func(e):
    """Transform the sums in an expression by calling ``.doit()``."""
    return e.replace(Sum, lambda *args: Sum(*args).doit())

