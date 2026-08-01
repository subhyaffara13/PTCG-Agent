
def _complex2real(z):
    return np.ascontiguousarray(z, dtype=complex).view(np.float64)

