
def _savez_compressed_dispatcher(file, *args, allow_pickle=True, **kwds):
    yield from args
    yield from kwds.values()

