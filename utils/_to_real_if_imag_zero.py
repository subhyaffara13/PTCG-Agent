
def _to_real_if_imag_zero(w, t):
    """Backwards compat helper: force w to be real if t.dtype is real and w.imag == 0
    """
    result_t = t.dtype.type
    if not isComplexType(result_t) and all(w.imag == 0.0):
        w = w.real
        result_t = _realType(result_t)
    else:
        result_t = _complexType(result_t)
    return w.astype(result_t, copy=False)

