
def _try_getclosurevars(func):
    try:
        return inspect.getclosurevars(func)
    except TypeError:
        return None

