
def _check_neg_zero(value):
    if value != 0.0:
        return False
    if not np.signbit(value.real):
        return False
    if value.dtype.kind == "c":
        return np.signbit(value.imag)
    return True

