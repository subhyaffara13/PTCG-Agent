
def _real2complex(x):
    return np.ascontiguousarray(x, dtype=float).view(np.complex128)

