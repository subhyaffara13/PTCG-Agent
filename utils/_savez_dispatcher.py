
def _savez_dispatcher(file, *args, allow_pickle=True, **kwds):
    yield from args
    yield from kwds.values()

