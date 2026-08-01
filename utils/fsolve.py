
def fsolve(func, x0, args=(), fprime=None, full_output=False,
           col_deriv=False, xtol=1.49012e-8, maxfev=0, band=None,
           epsfcn=None, factor=100, diag=None):
    """
    Find the roots of a function.

    Return the roots of the (non-linear) equations defined by
    ``func(x) = 0`` given a starting estimate.

    Parameters
    ----------
    func : callable ``f(x, *args)``
        A function that takes at least one (possibly vector) argument,
        and returns a value of the same length.
    x0 : ndarray
        The starting estimate for the roots of ``func(x) = 0``.
    args : tuple, optional
        Any extra arguments to `func`.
    fprime : callable ``f(x, *args)``, optional
        A function to compute the Jacobian of `func` with derivatives
        across the rows. By default, the Jacobian will be estimated.
    full_output : bool, optional
        If True, return optional outputs.
    col_deriv : bool, optional
        Specify whether the Jacobian function computes derivatives down
        the columns (faster, because there is no transpose operation).
    xtol : float, optional
        The calculation will terminate if the relative error between two
        consecutive iterates is at most `xtol`.
    maxfev : int, optional
        The maximum number of calls to the function. If zero, then
        ``100*(N+1)`` is the maximum where N is the number of elements
        in `x0`.
    band : tuple, optional
        If set to a two-sequence containing the number of sub- and
        super-diagonals within the band of the Jacobi matrix, the
        Jacobi matrix is considered banded (only for ``fprime=None``).
    epsfcn : float, optional
        A suitable step length for the forward-difference
        approximation of the Jacobian (for ``fprime=None``). If
        `epsfcn` is less than the machine precision, it is assumed
        that the relative errors in the functions are of the order of
        the machine precision.
    factor : float, optional
        A parameter determining the initial step bound
        (``factor * || diag * x||``). Should be in the interval
        ``(0.1, 100)``.
    diag : sequence, optional
        N positive entries that serve as a scale factors for the
        variables.

    Returns
    -------
    x : ndarray
        The solution (or the result of the last iteration for
        an unsuccessful call).
    infodict : dict
        A dictionary of optional outputs with the keys:

        ``nfev``
            number of function calls
        ``njev``
            number of Jacobian calls
        ``fvec``
            function evaluated at the output
        ``fjac``
            the orthogonal matrix, q, produced by the QR
            factorization of the final approximate Jacobian
            matrix, stored column wise
        ``r``
            upper triangular matrix produced by QR factorization
            of the same matrix
        ``qtf``
            the vector ``(transpose(q) * fvec)``

    ier : int
        An integer flag.  Set to 1 if a solution was found, otherwise refer
        to `mesg` for more information.
    mesg : str
        If no solution is found, `mesg` details the cause of failure.

    See Also
    --------
    root : Interface to root finding algorithms for multivariate
           functions. See the ``method='hybr'`` in particular.

    Notes
    -----
    ``fsolve`` is a wrapper around MINPACK's hybrd and hybrj algorithms.

    Examples
    --------
    Find a solution to the system of equations:
    ``x0*cos(x1) = 4,  x1*x0 - x1 = 5``.

    >>> import numpy as np
    >>> from scipy.optimize import fsolve
    >>> def func(x):
    ...     return [x[0] * np.cos(x[1]) - 4,
    ...             x[1] * x[0] - x[1] - 5]
    >>> root = fsolve(func, [1, 1])
    >>> root
    array([6.50409711, 0.90841421])
    >>> np.isclose(func(root), [0.0, 0.0])  # func(root) should be almost 0.0.
    array([ True,  True])

    """
    def _wrapped_func(*fargs):
        """
        Wrapped `func` to track the number of times
        the function has been called.
        """
        _wrapped_func.nfev += 1
        return func(*fargs)

    _wrapped_func.nfev = 0

    options = {'col_deriv': col_deriv,
               'xtol': xtol,
               'maxfev': maxfev,
               'band': band,
               'eps': epsfcn,
               'factor': factor,
               'diag': diag}

    res = _root_hybr(_wrapped_func, x0, args, jac=fprime, **options)
    res.nfev = _wrapped_func.nfev

    if full_output:
        x = res['x']
        info = {k: res.get(k)
                    for k in ('nfev', 'njev', 'fjac', 'r', 'qtf') if k in res}
        info['fvec'] = res['fun']
        return x, info, res['status'], res['message']
    else:
        status = res['status']
        msg = res['message']
        if status == 0:
            raise TypeError(msg)
        elif status == 1:
            pass
        elif status in [2, 3, 4, 5]:
            warnings.warn(msg, RuntimeWarning, stacklevel=2)
        else:
            raise TypeError(msg)
        return res['x']

