
def _gradient_dispatcher(f, *varargs, axis=None, edge_order=None):
    yield f
    yield from varargs

