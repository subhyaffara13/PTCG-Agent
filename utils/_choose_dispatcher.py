
def _choose_dispatcher(a, choices, out=None, mode=None):
    yield a
    yield from choices
    yield out

