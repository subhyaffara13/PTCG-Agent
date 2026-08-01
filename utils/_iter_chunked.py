
def _iter_chunked(x0, x1, chunksize=4, inc=1):
    """Iterate from x0 to x1 in chunks of chunksize and steps inc.

    x0 must be finite, x1 need not be. In the latter case, the iterator is
    infinite.
    Handles both x0 < x1 and x0 > x1. In the latter case, iterates downwards
    (make sure to set inc < 0.)

    >>> from scipy.stats._distn_infrastructure import _iter_chunked
    >>> [x for x in _iter_chunked(2, 5, inc=2)]
    [array([2, 4])]
    >>> [x for x in _iter_chunked(2, 11, inc=2)]
    [array([2, 4, 6, 8]), array([10])]
    >>> [x for x in _iter_chunked(2, -5, inc=-2)]
    [array([ 2,  0, -2, -4])]
    >>> [x for x in _iter_chunked(2, -9, inc=-2)]
    [array([ 2,  0, -2, -4]), array([-6, -8])]

    """
    if inc == 0:
        raise ValueError('Cannot increment by zero.')
    if chunksize <= 0:
        raise ValueError(f'Chunk size must be positive; got {chunksize}.')

    s = 1 if inc > 0 else -1
    stepsize = abs(chunksize * inc)

    x = np.copy(x0)
    while (x - x1) * inc < 0:
        delta = min(stepsize, abs(x - x1))
        step = delta * s
        supp = np.arange(x, x + step, inc)
        x += step
        yield supp

