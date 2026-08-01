
def _reify(t, s):
    return map(partial(reify, s=s), t)


def _reify(t, s):
    return tuple(reify(iter(t), s))


def _reify(t, s):
    return list(reify(iter(t), s))


def _reify(d, s):
    return {k: reify(v, s) for k, v in d.items()}


def _reify(o, s):
    return o  # catch all, just return the object


def _reify(o, s):
    """Reify a Python ``slice`` object"""

    return slice(*reify((o.start, o.stop, o.step), s))

