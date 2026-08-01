
def _make_default(expr):
    # XXX: Catching TypeError like this is a bad way of distinguishing between
    # classes and instances. The logic using this function should be rewritten
    # somehow.
    try:
        ret = expr()
    except TypeError:
        ret = expr

    return ret


def _make_default(expr):
    # XXX: Catching TypeError like this is a bad way of distinguishing
    # instances from classes. The logic using this function should be
    # rewritten somehow.
    try:
        expr = expr()
    except TypeError:
        return expr

    return expr

