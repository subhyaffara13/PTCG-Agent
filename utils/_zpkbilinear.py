
def _zpkbilinear(z, p, k, fs):
    """Bilinear transformation to convert a filter from analog to digital."""

    degree = _relative_degree(z, p)

    fs2 = 2*fs

    # Bilinear transform the poles and zeros
    z_z = [(fs2 + z1) / (fs2 - z1) for z1 in z]
    p_z = [(fs2 + p1) / (fs2 - p1) for p1 in p]

    # Any zeros that were at infinity get moved to the Nyquist frequency
    z_z.extend([-1] * degree)

    # Compensate for gain change
    numer = _prod(fs2 - z1 for z1 in z)
    denom = _prod(fs2 - p1 for p1 in p)
    k_z = k * numer / denom

    return z_z, p_z, k_z.real

