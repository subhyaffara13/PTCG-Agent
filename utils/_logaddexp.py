
def _logaddexp(x1, x2, *, evaluate=True):
    return log(Add(exp(x1, evaluate=evaluate), exp(x2, evaluate=evaluate), evaluate=evaluate))


def _logaddexp(x, y, xp=None):
    # logaddexp that supports complex numbers
    xp = array_namespace(x, y) if xp is None else xp
    x, y = xp.broadcast_arrays(x, y)
    xy = xp.stack((x, y), axis=0)
    return special.logsumexp(xy, axis=0)

