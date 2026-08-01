
def root(arg, n, k=0, evaluate=None):
    r"""Returns the *k*-th *n*-th root of ``arg``.

    Parameters
    ==========

    k : int, optional
        Should be an integer in $\{0, 1, ..., n-1\}$.
        Defaults to the principal root if $0$.

    evaluate : bool, optional
        The parameter determines if the expression should be evaluated.
        If ``None``, its value is taken from
        ``global_parameters.evaluate``.

    Examples
    ========

    >>> from sympy import root, Rational
    >>> from sympy.abc import x, n

    >>> root(x, 2)
    sqrt(x)

    >>> root(x, 3)
    x**(1/3)

    >>> root(x, n)
    x**(1/n)

    >>> root(x, -Rational(2, 3))
    x**(-3/2)

    To get the k-th n-th root, specify k:

    >>> root(-2, 3, 2)
    -(-1)**(2/3)*2**(1/3)

    To get all n n-th roots you can use the rootof function.
    The following examples show the roots of unity for n
    equal 2, 3 and 4:

    >>> from sympy import rootof

    >>> [rootof(x**2 - 1, i) for i in range(2)]
    [-1, 1]

    >>> [rootof(x**3 - 1,i) for i in range(3)]
    [1, -1/2 - sqrt(3)*I/2, -1/2 + sqrt(3)*I/2]

    >>> [rootof(x**4 - 1,i) for i in range(4)]
    [-1, 1, -I, I]

    SymPy, like other symbolic algebra systems, returns the
    complex root of negative numbers. This is the principal
    root and differs from the text-book result that one might
    be expecting. For example, the cube root of -8 does not
    come back as -2:

    >>> root(-8, 3)
    2*(-1)**(1/3)

    The real_root function can be used to either make the principal
    result real (or simply to return the real root directly):

    >>> from sympy import real_root
    >>> real_root(_)
    -2
    >>> real_root(-32, 5)
    -2

    Alternatively, the n//2-th n-th root of a negative number can be
    computed with root:

    >>> root(-32, 5, 5//2)
    -2

    See Also
    ========

    sympy.polys.rootoftools.rootof
    sympy.core.intfunc.integer_nthroot
    sqrt, real_root

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Square_root
    .. [2] https://en.wikipedia.org/wiki/Real_root
    .. [3] https://en.wikipedia.org/wiki/Root_of_unity
    .. [4] https://en.wikipedia.org/wiki/Principal_value
    .. [5] https://mathworld.wolfram.com/CubeRoot.html

    """
    n = sympify(n)
    if k:
        return Mul(Pow(arg, S.One/n, evaluate=evaluate), S.NegativeOne**(2*k/n), evaluate=evaluate)
    return Pow(arg, 1/n, evaluate=evaluate)


def root(fun, x0, args=(), method='hybr', jac=None, tol=None, callback=None,
         options=None):
    r"""
    Find a root of a vector function.

    Parameters
    ----------
    fun : callable
        A vector function to find a root of.

        Suppose the callable has signature ``f0(x, *my_args, **my_kwargs)``, where
        ``my_args`` and ``my_kwargs`` are required positional and keyword arguments.
        Rather than passing ``f0`` as the callable, wrap it to accept
        only ``x``; e.g., pass ``fun=lambda x: f0(x, *my_args, **my_kwargs)`` as the
        callable, where ``my_args`` (tuple) and ``my_kwargs`` (dict) have been
        gathered before invoking this function.
    x0 : ndarray
        Initial guess.
    args : tuple, optional
        Extra arguments passed to the objective function and its Jacobian.
    method : str, optional
        Type of solver. Should be one of

        - 'hybr'             :ref:`(see here) <optimize.root-hybr>`
        - 'lm'               :ref:`(see here) <optimize.root-lm>`
        - 'broyden1'         :ref:`(see here) <optimize.root-broyden1>`
        - 'broyden2'         :ref:`(see here) <optimize.root-broyden2>`
        - 'anderson'         :ref:`(see here) <optimize.root-anderson>`
        - 'linearmixing'     :ref:`(see here) <optimize.root-linearmixing>`
        - 'diagbroyden'      :ref:`(see here) <optimize.root-diagbroyden>`
        - 'excitingmixing'   :ref:`(see here) <optimize.root-excitingmixing>`
        - 'krylov'           :ref:`(see here) <optimize.root-krylov>`
        - 'df-sane'          :ref:`(see here) <optimize.root-dfsane>`

    jac : bool or callable, optional
        If `jac` is a Boolean and is True, `fun` is assumed to return the
        value of Jacobian along with the objective function. If False, the
        Jacobian will be estimated numerically.
        `jac` can also be a callable returning the Jacobian of `fun`. In
        this case, it must accept the same arguments as `fun`.
    tol : float, optional
        Tolerance for termination. For detailed control, use solver-specific
        options.
    callback : function, optional
        Optional callback function. It is called on every iteration as
        ``callback(x, f)`` where `x` is the current solution and `f`
        the corresponding residual. For all methods but 'hybr' and 'lm'.
    options : dict, optional
        A dictionary of solver options. E.g., `xtol` or `maxiter`, see
        :obj:`show_options()` for details.

    Returns
    -------
    sol : OptimizeResult
        The solution represented as a ``OptimizeResult`` object.
        Important attributes are: ``x`` the solution array, ``success`` a
        Boolean flag indicating if the algorithm exited successfully and
        ``message`` which describes the cause of the termination. See
        `OptimizeResult` for a description of other attributes.

    See Also
    --------
    show_options : Additional options accepted by the solvers

    Notes
    -----
    This section describes the available solvers that can be selected by the
    'method' parameter. The default method is *hybr*.

    Method *hybr* uses a modification of the Powell hybrid method as
    implemented in MINPACK [1]_.

    Method *lm* solves the system of nonlinear equations in a least squares
    sense using a modification of the Levenberg-Marquardt algorithm as
    implemented in MINPACK [1]_.

    Method *df-sane* is a derivative-free spectral method. [3]_

    Methods *broyden1*, *broyden2*, *anderson*, *linearmixing*,
    *diagbroyden*, *excitingmixing*, *krylov* are inexact Newton methods,
    with backtracking or full line searches [2]_. Each method corresponds
    to a particular Jacobian approximations.

    - Method *broyden1* uses Broyden's first Jacobian approximation, it is
      known as Broyden's good method.
    - Method *broyden2* uses Broyden's second Jacobian approximation, it
      is known as Broyden's bad method.
    - Method *anderson* uses (extended) Anderson mixing.
    - Method *Krylov* uses Krylov approximation for inverse Jacobian. It
      is suitable for large-scale problem.
    - Method *diagbroyden* uses diagonal Broyden Jacobian approximation.
    - Method *linearmixing* uses a scalar Jacobian approximation.
    - Method *excitingmixing* uses a tuned diagonal Jacobian
      approximation.

    .. warning::

        The algorithms implemented for methods *diagbroyden*,
        *linearmixing* and *excitingmixing* may be useful for specific
        problems, but whether they will work may depend strongly on the
        problem.

    .. versionadded:: 0.11.0

    References
    ----------
    .. [1] More, Jorge J., Burton S. Garbow, and Kenneth E. Hillstrom.
       1980. User Guide for MINPACK-1.
    .. [2] C. T. Kelley. 1995. Iterative Methods for Linear and Nonlinear
       Equations. Society for Industrial and Applied Mathematics.
       :doi:`10.1137/1.9781611970944`
    .. [3] W. La Cruz, J.M. Martinez, M. Raydan.
       Math. Comp. 75, 1429 (2006).

    Examples
    --------
    The following functions define a system of nonlinear equations and its
    jacobian.

    >>> import numpy as np
    >>> def fun(x):
    ...     return [x[0]  + 0.5 * (x[0] - x[1])**3 - 1.0,
    ...             0.5 * (x[1] - x[0])**3 + x[1]]

    >>> def jac(x):
    ...     return np.array([[1 + 1.5 * (x[0] - x[1])**2,
    ...                       -1.5 * (x[0] - x[1])**2],
    ...                      [-1.5 * (x[1] - x[0])**2,
    ...                       1 + 1.5 * (x[1] - x[0])**2]])

    A solution can be obtained as follows.

    >>> from scipy import optimize
    >>> sol = optimize.root(fun, [0, 0], jac=jac, method='hybr')
    >>> sol.x
    array([ 0.8411639,  0.1588361])

    **Large problem**

    Suppose that we needed to solve the following integrodifferential
    equation on the square :math:`[0,1]\times[0,1]`:

    .. math::

       \nabla^2 P = 10 \left(\int_0^1\int_0^1\cosh(P)\,dx\,dy\right)^2

    with :math:`P(x,1) = 1` and :math:`P=0` elsewhere on the boundary of
    the square.

    The solution can be found using the ``method='krylov'`` solver:

    >>> from scipy import optimize
    >>> # parameters
    >>> nx, ny = 75, 75
    >>> hx, hy = 1./(nx-1), 1./(ny-1)

    >>> P_left, P_right = 0, 0
    >>> P_top, P_bottom = 1, 0

    >>> def residual(P):
    ...    d2x = np.zeros_like(P)
    ...    d2y = np.zeros_like(P)
    ...
    ...    d2x[1:-1] = (P[2:]   - 2*P[1:-1] + P[:-2]) / hx/hx
    ...    d2x[0]    = (P[1]    - 2*P[0]    + P_left)/hx/hx
    ...    d2x[-1]   = (P_right - 2*P[-1]   + P[-2])/hx/hx
    ...
    ...    d2y[:,1:-1] = (P[:,2:] - 2*P[:,1:-1] + P[:,:-2])/hy/hy
    ...    d2y[:,0]    = (P[:,1]  - 2*P[:,0]    + P_bottom)/hy/hy
    ...    d2y[:,-1]   = (P_top   - 2*P[:,-1]   + P[:,-2])/hy/hy
    ...
    ...    return d2x + d2y - 10*np.cosh(P).mean()**2

    >>> guess = np.zeros((nx, ny), float)
    >>> sol = optimize.root(residual, guess, method='krylov')
    >>> print('Residual: %g' % abs(residual(sol.x)).max())
    Residual: 5.7972e-06  # may vary

    >>> import matplotlib.pyplot as plt
    >>> x, y = np.mgrid[0:1:(nx*1j), 0:1:(ny*1j)]
    >>> plt.pcolormesh(x, y, sol.x, shading='gouraud')
    >>> plt.colorbar()
    >>> plt.show()

    """
    def _wrapped_fun(*fargs):
        """
        Wrapped `func` to track the number of times
        the function has been called.
        """
        _wrapped_fun.nfev += 1
        return fun(*fargs)

    _wrapped_fun.nfev = 0

    if not isinstance(args, tuple):
        args = (args,)

    meth = method.lower()
    if options is None:
        options = {}

    if callback is not None and meth in ('hybr', 'lm'):
        warn(f'Method {method} does not accept callback.',
             RuntimeWarning, stacklevel=2)

    # fun also returns the Jacobian
    if not callable(jac) and meth in ('hybr', 'lm'):
        if bool(jac):
            fun = MemoizeJac(fun)
            jac = fun.derivative
        else:
            jac = None

    # set default tolerances
    if tol is not None:
        options = dict(options)
        if meth in ('hybr', 'lm'):
            options.setdefault('xtol', tol)
        elif meth in ('df-sane',):
            options.setdefault('ftol', tol)
        elif meth in ('broyden1', 'broyden2', 'anderson', 'linearmixing',
                      'diagbroyden', 'excitingmixing', 'krylov'):
            options.setdefault('xtol', tol)
            options.setdefault('xatol', np.inf)
            options.setdefault('ftol', np.inf)
            options.setdefault('fatol', np.inf)

    if meth == 'hybr':
        sol = _root_hybr(_wrapped_fun, x0, args=args, jac=jac, **options)
    elif meth == 'lm':
        sol = _root_leastsq(_wrapped_fun, x0, args=args, jac=jac, **options)
    elif meth == 'df-sane':
        _warn_jac_unused(jac, method)
        sol = _root_df_sane(_wrapped_fun, x0, args=args, callback=callback,
                            **options)
    elif meth in ('broyden1', 'broyden2', 'anderson', 'linearmixing',
                  'diagbroyden', 'excitingmixing', 'krylov'):
        _warn_jac_unused(jac, method)
        sol = _root_nonlin_solve(_wrapped_fun, x0, args=args, jac=jac,
                                 _method=meth, _callback=callback,
                                 **options)
    else:
        raise ValueError(f'Unknown solver {method}')

    sol.nfev = _wrapped_fun.nfev
    return sol


def root(ctx, x, n, k=0):
    n = int(n)
    x = ctx.convert(x)
    if k:
        # Special case: there is an exact real root
        if (n & 1 and 2*k == n-1) and (not ctx.im(x)) and (ctx.re(x) < 0):
            return -ctx.root(-x, n)
        # Multiply by root of unity
        prec = ctx.prec
        try:
            ctx.prec += 10
            v = ctx.root(x, n, 0) * ctx._rootof1(k, n)
        finally:
            ctx.prec = prec
        return +v
    return ctx._nthroot(x, n)

