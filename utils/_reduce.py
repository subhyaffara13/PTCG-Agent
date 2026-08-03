import functools

def _reduce(cls):
    raise pickle.PickleError("ScriptFunction cannot be pickled")


def _reduce(func, seq, initial=None):
    if initial is None:
        return functools.reduce(func, seq)
    else:
        return functools.reduce(func, seq, initial)

