
def wrap_array_like(result):
    if type(result) is tuple:
        return tuple(ArrayLike(r) for r in result)
    else:
        return ArrayLike(result)

