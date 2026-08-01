
def fixed_quad(func, a, b, args=(), n=5):
    """
    Compute a definite integral using fixed-order Gaussian quadrature.

    Integrate `func` from `a` to `b` using Gaussian quadrature of
    order `n`.

    Parameters
    ----------
    func : callable
        A Python function or method to integrate (must accept vector inputs).
        If integrating a vector-valued function, the returned array must have
        shape ``(..., len(x))``.
    a : float
        Lower limit of integration.
    b : float
        Upper limit of integration.
    args : tuple, optional
        Extra arguments to pass to function, if any.
    n : int, optional
        Order of quadrature integration. Default is 5.

    Returns
    -------
    val : float
        Gaussian quadrature approximation to the integral
    none : None
        Statically returned value of None

    See Also
    --------
    quad : adaptive quadrature using QUADPACK
    dblquad : double integrals
    tplquad : triple integrals
    romb : integrators for sampled data
    simpson : integrators for sampled data
    cumulative_trapezoid : cumulative integration for sampled data

    Examples
    --------
    >>> from scipy import integrate
    >>> import numpy as np
    >>> f = lambda x: x**8
    >>> integrate.fixed_quad(f, 0.0, 1.0, n=4)
    (0.1110884353741496, None)
    >>> integrate.fixed_quad(f, 0.0, 1.0, n=5)
    (0.11111111111111102, None)
    >>> print(1/9.0)  # analytical result
    0.1111111111111111

    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=4)
    (0.9999999771971152, None)
    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=5)
    (1.000000000039565, None)
    >>> np.sin(np.pi/2)-np.sin(0)  # analytical result
    1.0

    """
    # `args` not necessarily numeric arrays, so don't pass to array_namespace/xp_promote
    xp = array_namespace(a, b)
    a, b = xp_promote(a, b, force_floating=True, xp=xp)
    x, w = _cached_roots_legendre(n)
    x, w = xp.asarray(x, dtype=a.dtype), xp.asarray(w, dtype=a.dtype)
    x = xp.real(x)
    if not is_lazy_array(a) and (xp.isinf(a) or xp.isinf(b)):
        raise ValueError("Gaussian quadrature is only available for "
                         "finite limits.")
    y = (b-a)*(x+1)/2.0 + a
    return (b-a)/2.0 * xp.sum(w*func(y, *args), axis=-1), None

