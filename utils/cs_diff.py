
def cs_diff(x, a, b, period=None, _cache=_cache):
    """
    Return (a,b)-cosh/sinh pseudo-derivative of a periodic sequence.

    If ``x_j`` and ``y_j`` are Fourier coefficients of periodic functions x
    and y, respectively, then::

      y_j = -sqrt(-1)*cosh(j*a*2*pi/period)/sinh(j*b*2*pi/period) * x_j
      y_0 = 0

    Parameters
    ----------
    x : array_like
        The array to take the pseudo-derivative from.
    a, b : float
        Defines the parameters of the cosh/sinh pseudo-differential
        operator.
    period : float, optional
        The period of the sequence. Default period is ``2*pi``.

    Returns
    -------
    cs_diff : ndarray
        Pseudo-derivative of periodic sequence `x`.

    Notes
    -----
    For even len(`x`), the Nyquist mode of `x` is taken as zero.

    """
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'cs_diff_cache'):
            _cache.cs_diff_cache = {}
        _cache = _cache.cs_diff_cache

    tmp = asarray(x)
    if iscomplexobj(tmp):
        return cs_diff(tmp.real, a, b, period, _cache) + \
               1j*cs_diff(tmp.imag, a, b, period, _cache)
    if period is not None:
        a = a*2*pi/period
        b = b*2*pi/period
    n = len(x)
    omega = _cache.get((n,a,b))
    if omega is None:
        if len(_cache) > 20:
            while _cache:
                _cache.popitem()

        def kernel(k,a=a,b=b):
            if k:
                return -cosh(a*k)/sinh(b*k)
            return 0
        omega = convolve.init_convolution_kernel(n,kernel,d=1)
        _cache[(n,a,b)] = omega
    overwrite_x = _datacopied(tmp, x)
    return convolve.convolve(tmp,omega,swap_real_imag=1,overwrite_x=overwrite_x)

