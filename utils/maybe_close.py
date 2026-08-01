
def maybe_close(f):
    @contextlib.contextmanager
    def empty():
        yield
        return

    if not f:
        return empty()

    return contextlib.closing(f)

