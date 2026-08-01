
def _piecewise_dispatcher(x, condlist, funclist, *args, **kw):
    yield x
    # support the undocumented behavior of allowing scalars
    if np.iterable(condlist):
        yield from condlist

