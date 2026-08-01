
def ihilbert(x, _cache=_cache):
    """
    Return inverse Hilbert transform of a periodic sequence x.

    If ``x_j`` and ``y_j`` are Fourier coefficients of periodic functions x
    and y, respectively, then::

      y_j = -sqrt(-1)*sign(j) * x_j
      y_0 = 0

    """  # numpydoc ignore=RT01
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'ihilbert_cache'):
            _cache.ihilbert_cache = {}
        _cache = _cache.ihilbert_cache
    return -hilbert(x, _cache)

