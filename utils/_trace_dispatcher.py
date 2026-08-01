
def _trace_dispatcher(x, /, *, offset=None, dtype=None):
    return (x,)


def _trace_dispatcher(
        a, offset=None, axis1=None, axis2=None, dtype=None, out=None):
    return (a, out)

