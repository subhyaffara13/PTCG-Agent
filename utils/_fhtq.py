
def _fhtq(a, u, inverse=False, *, xp=None):
    """Compute the biased fast Hankel transform.

    This is the basic FFTLog routine.
    """
    if xp is None:
        xp = np

    # size of transform
    n = a.shape[-1]

    # biased fast Hankel transform via real FFT
    A = rfft(a, axis=-1)
    if not inverse:
        # forward transform
        A *= u
    else:
        # backward transform
        A /= xp.conj(u)
    A = irfft(A, n, axis=-1)
    A = xp.flip(A, axis=-1)

    return A

