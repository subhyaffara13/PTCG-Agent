
def ismatrix(t) -> bool:
    return ((isinstance(t, list | tuple) and
             len(t) > 0 and issequence(t[0])) or
            (isinstance(t, np.ndarray) and t.ndim == 2))

