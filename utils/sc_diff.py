
def sc_diff(x, a, b, period=None, _cache=_cache):
    """
    Return (a,b)-sinh/cosh pseudo-derivative of a periodic sequence x.

    If x_j and y_j are Fourier coefficients of periodic functions x
    and y, respectively, then::

      y_j = sqrt(-1)*sinh(j*a*2*pi/period)/cosh(j*b*2*pi/period) * x_j
      y_0 = 0

    Parameters
    ----------
    x : array_like
        Input array.
    a, b : float
        Defines the parameters of the sinh/cosh pseudo-differential
        operator.
    period : float, optional
        The period of the sequence x. Default is 2*pi.

    Notes
    -----
    ``sc_diff(cs_diff(x,a,b),b,a) == x``
    For even ``len(x)``, the Nyquist mode of x is taken as zero.

    """  # numpydoc ignore=RT01
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'sc_diff_cache'):
            _cache.sc_diff_cache = {}
        _cache = _cache.sc_diff_cache

    tmp = asarray(x)
    if iscomplexobj(tmp):
        return sc_diff(tmp.real, a, b, period, _cache) + \
               1j * sc_diff(tmp.imag, a, b, period, _cache)
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
                return sinh(a*k)/cosh(b*k)
            return 0
        omega = convolve.init_convolution_kernel(n,kernel,d=1)
        _cache[(n,a,b)] = omega
    overwrite_x = _datacopied(tmp, x)
    return convolve.convolve(tmp,omega,swap_real_imag=1,overwrite_x=overwrite_x)

