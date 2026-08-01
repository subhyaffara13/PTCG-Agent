
def line_search_wolfe2(f, myfprime, xk, pk, gfk=None, old_fval=None,
                       old_old_fval=None, args=(), c1=1e-4, c2=0.9, amax=None,
                       extra_condition=None, maxiter=10):
    """Find alpha that satisfies strong Wolfe conditions.

    Parameters
    ----------
    f : callable f(x,*args)
        Objective function.
    myfprime : callable f'(x,*args)
        Objective function gradient.
    xk : ndarray
        Starting point.
    pk : ndarray
        Search direction. The search direction must be a descent direction
        for the algorithm to converge.
    gfk : ndarray, optional
        Gradient value for x=xk (xk being the current parameter
        estimate). Will be recomputed if omitted.
    old_fval : float, optional
        Function value for x=xk. Will be recomputed if omitted.
    old_old_fval : float, optional
        Function value for the point preceding x=xk.
    args : tuple, optional
        Additional arguments passed to objective function.
    c1 : float, optional
        Parameter for Armijo condition rule.
    c2 : float, optional
        Parameter for curvature condition rule.
    amax : float, optional
        Maximum step size
    extra_condition : callable, optional
        A callable of the form ``extra_condition(alpha, x, f, g)``
        returning a boolean. Arguments are the proposed step ``alpha``
        and the corresponding ``x``, ``f`` and ``g`` values. The line search
        accepts the value of ``alpha`` only if this
        callable returns ``True``. If the callable returns ``False``
        for the step length, the algorithm will continue with
        new iterates. The callable is only called for iterates
        satisfying the strong Wolfe conditions.
    maxiter : int, optional
        Maximum number of iterations to perform.

    Returns
    -------
    alpha : float or None
        Alpha for which ``x_new = x0 + alpha * pk``,
        or None if the line search algorithm did not converge.
    fc : int
        Number of function evaluations made.
    gc : int
        Number of gradient evaluations made.
    new_fval : float or None
        New function value ``f(x_new)=f(x0+alpha*pk)``,
        or None if the line search algorithm did not converge.
    old_fval : float
        Old function value ``f(x0)``.
    new_slope : float or None
        The local slope along the search direction at the
        new value ``<myfprime(x_new), pk>``,
        or None if the line search algorithm did not converge.


    Notes
    -----
    Uses the line search algorithm to enforce strong Wolfe conditions. See algorithms
    3.5 and 3.6 on pp. 60-61 in [1]_ (first edition, algorithms 3.2 and 3.3 on
    pp. 59-61), see also [2]_.

    The search direction `pk` must be a descent direction (e.g.
    ``-myfprime(xk)``) to find a step length that satisfies the strong Wolfe
    conditions. If the search direction is not a descent direction (e.g.
    ``myfprime(xk)``), then `alpha`, `new_fval`, and `new_slope` will be None.

    References
    ----------
    .. [1] J. Nocedal and S. J. Wright. "Numerical Optimization". Springer Ser.
       Oper. Res. Financ. Eng. Springer, New York, NY, USA, second edition,
       2006. doi:`10.1007/978-0-387-40065-5`
    .. [2] R. Fletcher, "Practical Methods of Optimization." Wiley, May 23, 2000.
       doi:`10.1002/9781118723203`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize import line_search

    An objective function and its gradient are defined.

    >>> def obj_func(x):
    ...     return (x[0])**2+(x[1])**2
    >>> def obj_grad(x):
    ...     return [2*x[0], 2*x[1]]

    We can find alpha that satisfies strong Wolfe conditions.

    >>> start_point = np.array([1.8, 1.7])
    >>> search_gradient = np.array([-1.0, -1.0])
    >>> line_search(obj_func, obj_grad, start_point, search_gradient)
    (1.0, 2, 1, 1.1300000000000001, 6.13, [1.6, 1.4])

    """
    fc = [0]
    gc = [0]
    gval = [None]
    gval_alpha = [None]

    def phi(alpha):
        fc[0] += 1
        return f(xk + alpha * pk, *args)

    fprime = myfprime

    def derphi(alpha):
        gc[0] += 1
        gval[0] = fprime(xk + alpha * pk, *args)  # store for later use
        gval_alpha[0] = alpha
        return np.dot(gval[0], pk)

    if gfk is None:
        gfk = fprime(xk, *args)
    derphi0 = np.dot(gfk, pk)

    if extra_condition is not None:
        # Add the current gradient as argument, to avoid needless
        # re-evaluation
        def extra_condition2(alpha, phi):
            if gval_alpha[0] != alpha:
                derphi(alpha)
            x = xk + alpha * pk
            return extra_condition(alpha, x, phi, gval[0])
    else:
        extra_condition2 = None

    alpha_star, phi_star, old_fval, derphi_star = scalar_search_wolfe2(
            phi, derphi, old_fval, old_old_fval, derphi0, c1, c2, amax,
            extra_condition2, maxiter=maxiter)

    if derphi_star is None:
        warn('The line search algorithm did not converge',
             LineSearchWarning, stacklevel=2)
    else:
        # derphi_star is a number (derphi) -- so use the most recently
        # calculated gradient used in computing it derphi = gfk*pk
        # this is the gradient at the next step no need to compute it
        # again in the outer loop.
        derphi_star = gval[0]

    return alpha_star, fc[0], gc[0], phi_star, old_fval, derphi_star

