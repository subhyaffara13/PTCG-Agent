import itertools

def exc_iter(*args):
    """
    Iterate over Cartesian product of *args, and if an exception is raised,
    add information of the current iterate.
    """

    value = [None]

    def iterate():
        for v in itertools.product(*args):
            value[0] = v
            yield v

    try:
        yield iterate()
    except Exception:
        import traceback
        msg = f"At: {repr(value[0])!r}\n{traceback.format_exc()}"
        raise AssertionError(msg)

