
def _fiinfo(x):
    if np.issubdtype(x.dtype, np.inexact):
        return np.finfo(x.dtype)
    else:
        return np.iinfo(x)

