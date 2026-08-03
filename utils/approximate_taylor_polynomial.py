import os

def approximate_taylor_polynomial(f,x,degree,scale,order=None):
    """
    Estimate the Taylor polynomial of f at x by polynomial fitting.

    .. deprecated:: 1.18.0
        This function is deprecated and will be removed in SciPy 1.20.0. Use the
        following code instead:

        .. code-block:: python

            import numpy as np

            def f(z): return np.exp(z**2)  # example function
            N = 10  # number of terms in the Taylor expansion
            zz = np.exp(2j * np.pi * np.arange(N) / N)  # roots of unity
            c = np.fft.fft(f(zz)) / N
            c = np.real(c)  # c must be real by symmetry


    Parameters
    ----------
    f : callable
        The function whose Taylor polynomial is sought. Should accept
        a vector of `x` values.
    x : scalar
        The point at which the polynomial is to be evaluated.
    degree : int
        The degree of the Taylor polynomial
    scale : scalar
        The width of the interval to use to evaluate the Taylor polynomial.
        Function values spread over a range this wide are used to fit the
        polynomial. Must be chosen carefully.
    order : int or None, optional
        The order of the polynomial to be used in the fitting; `f` will be
        evaluated ``order+1`` times. If None, use `degree`.

    Returns
    -------
    p : poly1d instance
        The Taylor polynomial (translated to the origin, so that
        for example p(0)=f(x)).

    Notes
    -----
    The appropriate choice of "scale" is a trade-off; too large and the
    function differs from its Taylor polynomial too much to get a good
    answer, too small and round-off errors overwhelm the higher-order terms.
    The algorithm used becomes numerically unstable around order 30 even
    under ideal circumstances.

    Choosing order somewhat larger than degree may improve the higher-order
    terms.

    Examples
    --------
    We can calculate Taylor approximation polynomials of sin function with
    various degrees:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.interpolate import approximate_taylor_polynomial
    >>> x = np.linspace(-10.0, 10.0, num=100)
    >>> plt.plot(x, np.sin(x), label="sin curve")
    >>> for degree in np.arange(1, 15, step=2):
    ...     sin_taylor = approximate_taylor_polynomial(np.sin, 0, degree, 1,
    ...                                                order=degree + 2)
    ...     plt.plot(x, sin_taylor(x), label=f"degree={degree}")
    >>> plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
    ...            borderaxespad=0.0, shadow=True)
    >>> plt.tight_layout()
    >>> plt.axis([-10, 10, -10, 10])
    >>> plt.show()

    """
    _warn_skips = (os.path.dirname(__file__),)
    msg = ("`approximate_taylor_polynomial` is deprecated and will be removed in "
           "SciPy 1.20.0.")
    warnings.warn(msg, DeprecationWarning, skip_file_prefixes=_warn_skips)
    if order is None:
        order = degree

    n = order+1
    # Choose n points that cluster near the endpoints of the interval in
    # a way that avoids the Runge phenomenon. Ensure, by including the
    # endpoint or not as appropriate, that one point always falls at x
    # exactly.
    xs = scale*np.cos(np.linspace(0,np.pi,n,endpoint=n % 1)) + x

    P = KroghInterpolator(xs, f(xs))
    d = P.derivatives(x,der=degree+1)

    return np.poly1d((d/factorial(np.arange(degree+1)))[::-1])

