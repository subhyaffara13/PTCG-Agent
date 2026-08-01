
def _eps_cast(dtyp):
    """Get the epsilon for dtype, possibly downcast to BLAS types."""
    dt = dtyp
    if dt == np.longdouble:
        dt = np.float64
    elif dt == np.clongdouble:
        dt = np.complex128
    return np.finfo(dt).eps

