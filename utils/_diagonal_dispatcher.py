
def _diagonal_dispatcher(x, /, *, offset=None):
    return (x,)


def _diagonal_dispatcher(a, offset=None, axis1=None, axis2=None):
    return (a,)

