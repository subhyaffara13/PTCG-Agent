
def _cross_dispatcher(x1, x2, /, *, axis=None):
    return (x1, x2,)


def _cross_dispatcher(a, b, axisa=None, axisb=None, axisc=None, axis=None):
    return (a, b)

