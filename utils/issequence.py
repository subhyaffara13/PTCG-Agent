
def issequence(x: object) -> TypeGuard[collections.abc.Sequence[object]]:
    return isinstance(x, collections.abc.Sequence) and not isinstance(x, str)


def issequence(t) -> bool:
    return ((isinstance(t, list | tuple) and
            (len(t) == 0 or np.isscalar(t[0]))) or
            (isinstance(t, np.ndarray) and (t.ndim == 1)))


def issequence(seq):
    """
    Is seq a sequence (ndarray, list or tuple)?

    """
    return isinstance(seq, (ndarray, tuple, list))

