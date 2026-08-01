
def ensure_list(thing):
    """
    Wrap ``thing`` in a list if it's a single str.

    Otherwise, return it unchanged.
    """
    if isinstance(thing, str):
        return [thing]
    return thing


def ensure_list(xs):
  return xs if type(xs) is list else list(xs)

