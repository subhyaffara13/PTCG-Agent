
def _tensordot_dispatcher(x1, x2, /, *, axes=None):
    return (x1, x2)


def _tensordot_dispatcher(a, b, axes=None):
    return (a, b)

