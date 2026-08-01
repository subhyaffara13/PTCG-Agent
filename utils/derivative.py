
def derivative(f, x, *, args=(), kwargs=None, tolerances=None, maxiter=10,
               order=8, initial_step=0.5, step_factor=2.0,
               step_direction=0, preserve_shape=False, callback=None):
    """Evaluate the derivative of an elementwise, real scalar function numerically.

    For each element of the output of `f`, `derivative` approximates the first
    derivative of `f` at the corresponding element of `x` using finite difference
    differentiation.

    This function works elementwise when `x`, `step_direction`, and `args` contain
    (broadcastable) arrays.

    Parameters
    ----------
    f : callable
        The function whose derivative is desired. The signature must be::

            f(xi: ndarray, *argsi) -> ndarray

        where each element of ``xi`` is a finite real number and ``argsi`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable with
        ``xi``. `f` must be an elementwise function: each scalar element ``f(xi)[j]``
        must equal ``f(xi[j])`` for valid indices ``j``. It must not mutate the array
        ``xi`` or the arrays in ``argsi``.
    x : float array_like
        Abscissae at which to evaluate the derivative. Must be broadcastable with
        `args` and `step_direction`.
    args : tuple of array_like, optional
        Additional positional array arguments to be passed to `f`. Arrays
        must be broadcastable with one another and the arrays of `init`.
        If the callable for which the root is desired requires arguments that are
        not broadcastable with `x`, wrap that callable with `f` such that `f`
        accepts only `x` and broadcastable ``*args``.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `f`. See `args`.
    tolerances : dictionary of floats, optional
        Absolute and relative tolerances. Valid keys of the dictionary are:

        - ``atol`` - absolute tolerance on the derivative
        - ``rtol`` - relative tolerance on the derivative

        Iteration will stop when ``res.error < atol + rtol * abs(res.df)``. The default
        `atol` is the smallest normal number of the appropriate dtype, and
        the default `rtol` is the square root of the precision of the
        appropriate dtype.
    maxiter : int, default: 10
        The maximum number of iterations of the algorithm to perform. See Notes.
    order : int, default: 8
        The (positive integer) order of the finite difference formula to be
        used. Odd integers will be rounded up to the next even integer.
    initial_step : float array_like, default: 0.5
        The (absolute) initial step size for the finite difference derivative
        approximation.
    step_factor : float, default: 2.0
        The factor by which the step size is *reduced* in each iteration; i.e.
        the step size in iteration 1 is ``initial_step/step_factor``. If
        ``step_factor < 1``, subsequent steps will be greater than the initial
        step; this may be useful if steps smaller than some threshold are
        undesirable (e.g. due to subtractive cancellation error).
    step_direction : int array_like
        An array representing the direction of the finite difference steps (for
        use when `x` lies near to the boundary of the domain of the function.)
        Must be broadcastable with `x` and all `args`.
        Where 0 (default), central differences are used; where negative (e.g.
        -1), steps are non-positive; and where positive (e.g. 1), all steps are
        non-negative.
    preserve_shape : bool, default: False
        In the following, "arguments of `f`" refers to the array ``xi`` and
        any arrays within ``argsi``. Let ``shape`` be the broadcasted shape
        of `x` and all elements of `args` (which is conceptually
        distinct from ``xi` and ``argsi`` passed into `f`).

        - When ``preserve_shape=False`` (default), `f` must accept arguments
          of *any* broadcastable shapes.

        - When ``preserve_shape=True``, `f` must accept arguments of shape
          ``shape`` *or* ``shape + (n,)``, where ``(n,)`` is the number of
          abscissae at which the function is being evaluated.

        In either case, for each scalar element ``xi[j]`` within ``xi``, the array
        returned by `f` must include the scalar ``f(xi[j])`` at the same index.
        Consequently, the shape of the output is always the shape of the input
        ``xi``.

        See Examples.
    callback : callable, optional
        An optional user-supplied function to be called before the first
        iteration and after each iteration.
        Called as ``callback(res)``, where ``res`` is a ``_RichResult``
        similar to that returned by `derivative` (but containing the current
        iterate's values of all variables). If `callback` raises a
        ``StopIteration``, the algorithm will terminate immediately and
        `derivative` will return a result. `callback` must not mutate
        `res` or its attributes.

    Returns
    -------
    res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes. The descriptions are written as though the values will
        be scalars; however, if `f` returns an array, the outputs will be
        arrays of the same shape.

        success : bool array
            ``True`` where the algorithm terminated successfully (status ``0``);
            ``False`` otherwise.
        status : int array
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm converged to the specified tolerances.
            - ``-1`` : The error estimate increased, so iteration was terminated.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``1`` : The algorithm is proceeding normally (in `callback` only).

        df : float array
            The derivative of `f` at `x`, if the algorithm terminated
            successfully.
        error : float array
            An estimate of the error: the magnitude of the difference between
            the current estimate of the derivative and the estimate in the
            previous iteration.
        nit : int array
            The number of iterations of the algorithm that were performed.
        nfev : int array
            The number of points at which `f` was evaluated.
        x : float array
            The value at which the derivative of `f` was evaluated
            (after broadcasting with `args` and `step_direction`).

    See Also
    --------
    jacobian, hessian

    Notes
    -----
    The implementation was inspired by jacobi [1]_, numdifftools [2]_, and
    DERIVEST [3]_, but the implementation follows the theory of Taylor series
    more straightforwardly (and arguably naively so).
    In the first iteration, the derivative is estimated using a finite
    difference formula of order `order` with maximum step size `initial_step`.
    Each subsequent iteration, the maximum step size is reduced by
    `step_factor`, and the derivative is estimated again until a termination
    condition is reached. The error estimate is the magnitude of the difference
    between the current derivative approximation and that of the previous
    iteration.

    The stencils of the finite difference formulae are designed such that
    abscissae are "nested": after `f` is evaluated at ``order + 1``
    points in the first iteration, `f` is evaluated at only two new points
    in each subsequent iteration; ``order - 1`` previously evaluated function
    values required by the finite difference formula are reused, and two
    function values (evaluations at the points furthest from `x`) are unused.

    Step sizes are absolute. When the step size is small relative to the
    magnitude of `x`, precision is lost; for example, if `x` is ``1e20``, the
    default initial step size of ``0.5`` cannot be resolved. Accordingly,
    consider using larger initial step sizes for large magnitudes of `x`.

    The default tolerances are challenging to satisfy at points where the
    true derivative is exactly zero. If the derivative may be exactly zero,
    consider specifying an absolute tolerance (e.g. ``atol=1e-12``) to
    improve convergence.

    References
    ----------
    .. [1] Hans Dembinski (@HDembinski). jacobi.
           https://github.com/HDembinski/jacobi
    .. [2] Per A. Brodtkorb and John D'Errico. numdifftools.
           https://numdifftools.readthedocs.io/en/latest/
    .. [3] John D'Errico. DERIVEST: Adaptive Robust Numerical Differentiation.
           https://www.mathworks.com/matlabcentral/fileexchange/13490-adaptive-robust-numerical-differentiation
    .. [4] Numerical Differentition. Wikipedia.
           https://en.wikipedia.org/wiki/Numerical_differentiation

    Examples
    --------
    Evaluate the derivative of ``np.exp`` at several points ``x``.

    >>> import numpy as np
    >>> from scipy.differentiate import derivative
    >>> f = np.exp
    >>> df = np.exp  # true derivative
    >>> x = np.linspace(1, 2, 5)
    >>> res = derivative(f, x)
    >>> res.df  # approximation of the derivative
    array([2.71828183, 3.49034296, 4.48168907, 5.75460268, 7.3890561 ])
    >>> res.error  # estimate of the error
    array([7.13740178e-12, 9.16600129e-12, 1.17594823e-11, 1.51061386e-11,
           1.94262384e-11])
    >>> abs(res.df - df(x))  # true error
    array([2.53130850e-14, 3.55271368e-14, 5.77315973e-14, 5.59552404e-14,
           6.92779167e-14])

    Show the convergence of the approximation as the step size is reduced.
    Each iteration, the step size is reduced by `step_factor`, so for
    sufficiently small initial step, each iteration reduces the error by a
    factor of ``1/step_factor**order`` until finite precision arithmetic
    inhibits further improvement.

    >>> import matplotlib.pyplot as plt
    >>> iter = list(range(1, 12))  # maximum iterations
    >>> hfac = 2  # step size reduction per iteration
    >>> hdir = [-1, 0, 1]  # compare left-, central-, and right- steps
    >>> order = 4  # order of differentiation formula
    >>> x = 1
    >>> ref = df(x)
    >>> errors = []  # true error
    >>> for i in iter:
    ...     res = derivative(f, x, maxiter=i, step_factor=hfac,
    ...                      step_direction=hdir, order=order,
    ...                      # prevent early termination
    ...                      tolerances=dict(atol=0, rtol=0))
    ...     errors.append(abs(res.df - ref))
    >>> errors = np.array(errors)
    >>> plt.semilogy(iter, errors[:, 0], label='left differences')
    >>> plt.semilogy(iter, errors[:, 1], label='central differences')
    >>> plt.semilogy(iter, errors[:, 2], label='right differences')
    >>> plt.xlabel('iteration')
    >>> plt.ylabel('error')
    >>> plt.legend()
    >>> plt.show()
    >>> (errors[1, 1] / errors[0, 1], 1 / hfac**order)
    (0.06215223140159822, 0.0625)

    The implementation is vectorized over `x`, `step_direction`, and `args`.
    The function is evaluated once before the first iteration to perform input
    validation and standardization, and once per iteration thereafter.

    >>> def f(x, p):
    ...     f.nit += 1
    ...     return x**p
    >>> f.nit = 0
    >>> def df(x, p):
    ...     return p*x**(p-1)
    >>> x = np.arange(1, 5)
    >>> p = np.arange(1, 6).reshape((-1, 1))
    >>> hdir = np.arange(-1, 2).reshape((-1, 1, 1))
    >>> res = derivative(f, x, args=(p,), step_direction=hdir, maxiter=1)
    >>> np.allclose(res.df, df(x, p))
    True
    >>> res.df.shape
    (3, 5, 4)
    >>> f.nit
    2

    By default, `preserve_shape` is False, and therefore the callable
    `f` may be called with arrays of any broadcastable shapes.
    For example:

    >>> shapes = []
    >>> def f(x, c):
    ...    shape = np.broadcast_shapes(x.shape, c.shape)
    ...    shapes.append(shape)
    ...    return np.sin(c*x)
    >>>
    >>> c = [1, 5, 10, 20]
    >>> res = derivative(f, 0, args=(c,))
    >>> shapes
    [(4,), (4, 8), (4, 2), (3, 2), (2, 2), (1, 2)]

    To understand where these shapes are coming from - and to better
    understand how `derivative` computes accurate results - note that
    higher values of ``c`` correspond with higher frequency sinusoids.
    The higher frequency sinusoids make the function's derivative change
    faster, so more function evaluations are required to achieve the target
    accuracy:

    >>> res.nfev
    array([11, 13, 15, 17], dtype=int32)

    The initial ``shape``, ``(4,)``, corresponds with evaluating the
    function at a single abscissa and all four frequencies; this is used
    for input validation and to determine the size and dtype of the arrays
    that store results. The next shape corresponds with evaluating the
    function at an initial grid of abscissae and all four frequencies.
    Successive calls to the function evaluate the function at two more
    abscissae, increasing the effective order of the approximation by two.
    However, in later function evaluations, the function is evaluated at
    fewer frequencies because the corresponding derivative has already
    converged to the required tolerance. This saves function evaluations to
    improve performance, but it requires the function to accept arguments of
    any shape.

    "Vector-valued" functions are unlikely to satisfy this requirement.
    For example, consider

    >>> def f(x):
    ...    return [x, np.sin(3*x), x+np.sin(10*x), np.sin(20*x)*(x-1)**2]

    This integrand is not compatible with `derivative` as written; for instance,
    the shape of the output will not be the same as the shape of ``x``. Such a
    function *could* be converted to a compatible form with the introduction of
    additional parameters, but this would be inconvenient. In such cases,
    a simpler solution would be to use `preserve_shape`.

    >>> shapes = []
    >>> def f(x):
    ...     shapes.append(x.shape)
    ...     x0, x1, x2, x3 = x
    ...     return [x0, np.sin(3*x1), x2+np.sin(10*x2), np.sin(20*x3)*(x3-1)**2]
    >>>
    >>> x = np.zeros(4)
    >>> res = derivative(f, x, preserve_shape=True)
    >>> shapes
    [(4,), (4, 8), (4, 2), (4, 2), (4, 2), (4, 2)]

    Here, the shape of ``x`` is ``(4,)``. With ``preserve_shape=True``, the
    function may be called with argument ``x`` of shape ``(4,)`` or ``(4, n)``,
    and this is what we observe.

    """
    # TODO (followup):
    #  - investigate behavior at saddle points
    #  - multivariate functions?
    #  - relative steps?
    #  - show example of `np.vectorize`

    res = _derivative_iv(f, x, args, kwargs, tolerances, maxiter, order, initial_step,
                         step_factor, step_direction, preserve_shape, callback)
    (func, x, args, kwargs, atol, rtol, maxiter, order,
     h0, fac, hdir, preserve_shape, callback) = res

    # Initialization
    # Since f(x) (no step) is not needed for central differences, it may be
    # possible to eliminate this function evaluation. However, it's useful for
    # input validation and standardization, and everything else is designed to
    # reduce function calls, so let's keep it simple.
    temp = eim._initialize(func, (x,), args, kwargs=kwargs,
                           preserve_shape=preserve_shape)
    func, xs, fs, args, shape, dtype, xp = temp

    finfo = xp.finfo(dtype)
    atol = finfo.smallest_normal if atol is None else atol
    rtol = finfo.eps**0.5 if rtol is None else rtol  # keep same as `hessian`

    x, f = xs[0], fs[0]
    df = xp.full_like(f, xp.nan)

    # Ideally we'd broadcast the shape of `hdir` in `_elementwise_algo_init`, but
    # it's simpler to do it here than to generalize `_elementwise_algo_init` further.
    # `hdir` and `x` are already broadcasted in `_derivative_iv`, so we know
    # that `hdir` can be broadcasted to the final shape. Same with `h0`.
    hdir = xp.broadcast_to(hdir, shape)
    hdir = xp.reshape(hdir, (-1,))
    hdir = xp.astype(xp.sign(hdir), dtype)
    h0 = xp.broadcast_to(h0, shape)
    h0 = xp.reshape(h0, (-1,))
    h0 = xp.astype(h0, dtype)
    h0 = xpx.at(h0)[h0 <= 0].set(xp.nan)

    status = xp.full_like(x, eim._EINPROGRESS, dtype=xp.int32)  # in progress
    nit, nfev = 0, 1  # one function evaluations performed above
    # Boolean indices of left, central, right, and (all) one-sided steps
    il = hdir < 0
    ic = hdir == 0
    ir = hdir > 0
    io = il | ir

    # Most of these attributes are reasonably obvious, but:
    # - `fs` holds all the function values of all active `x`. The zeroth
    #   axis corresponds with active points `x`, the first axis corresponds
    #   with the different steps (in the order described in
    #   `_derivative_weights`).
    # - `terms` (which could probably use a better name) is half the `order`,
    #   which is always even.
    work = _RichResult(x=x, df=df, fs=f[:, xp.newaxis], error=xp.nan, h=h0,
                       df_last=xp.nan, error_last=xp.nan, fac=fac,
                       atol=atol, rtol=rtol, nit=nit, nfev=nfev,
                       status=status, dtype=dtype, terms=(order+1)//2,
                       hdir=hdir, il=il, ic=ic, ir=ir, io=io,
                       # Store the weights in an object so they can't get compressed
                       # Using RichResult to allow dot notation, but a dict would work
                       diff_state=_RichResult(central=[], right=[], fac=None))

    # This is the correspondence between terms in the `work` object and the
    # final result. In this case, the mapping is trivial. Note that `success`
    # is prepended automatically.
    res_work_pairs = [('status', 'status'), ('df', 'df'), ('error', 'error'),
                      ('nit', 'nit'), ('nfev', 'nfev'), ('x', 'x')]

    def pre_func_eval(work):
        """Determine the abscissae at which the function needs to be evaluated.

        See `_derivative_weights` for a description of the stencil (pattern
        of the abscissae).

        In the first iteration, there is only one stored function value in
        `work.fs`, `f(x)`, so we need to evaluate at `order` new points. In
        subsequent iterations, we evaluate at two new points. Note that
        `work.x` is always flattened into a 1D array after broadcasting with
        all `args`, so we add a new axis at the end and evaluate all point
        in one call to the function.

        For improvement:
        - Consider measuring the step size actually taken, since ``(x + h) - x``
          is not identically equal to `h` with floating point arithmetic.
        - Adjust the step size automatically if `x` is too big to resolve the
          step.
        - We could probably save some work if there are no central difference
          steps or no one-sided steps.
        """
        n = work.terms  # half the order
        h = work.h[:, xp.newaxis]  # step size
        c = work.fac  # step reduction factor
        d = c**0.5  # square root of step reduction factor (one-sided stencil)
        # Note - no need to be careful about dtypes until we allocate `x_eval`

        if work.nit == 0:
            hc = h / c**xp.arange(n, dtype=work.dtype)
            hc = xp.concat((-xp.flip(hc, axis=-1), hc), axis=-1)
        else:
            hc = xp.concat((-h, h), axis=-1) / c**(n-1)

        if work.nit == 0:
            hr = h / d**xp.arange(2*n, dtype=work.dtype)
        else:
            hr = xp.concat((h, h/d), axis=-1) / c**(n-1)

        n_new = 2*n if work.nit == 0 else 2  # number of new abscissae
        x_eval = xp.zeros((work.hdir.shape[0], n_new), dtype=work.dtype)
        il, ic, ir = work.il, work.ic, work.ir
        x_eval = xpx.at(x_eval)[ir].set(work.x[ir][:, xp.newaxis] + hr[ir])
        x_eval = xpx.at(x_eval)[ic].set(work.x[ic][:, xp.newaxis] + hc[ic])
        x_eval = xpx.at(x_eval)[il].set(work.x[il][:, xp.newaxis] - hr[il])
        return x_eval

    def post_func_eval(x, f, work):
        """ Estimate the derivative and error from the function evaluations

        As in `pre_func_eval`: in the first iteration, there is only one stored
        function value in `work.fs`, `f(x)`, so we need to add the `order` new
        points. In subsequent iterations, we add two new points. The tricky
        part is getting the order to match that of the weights, which is
        described in `_derivative_weights`.

        For improvement:
        - Change the order of the weights (and steps in `pre_func_eval`) to
          simplify `work_fc` concatenation and eliminate `fc` concatenation.
        - It would be simple to do one-step Richardson extrapolation with `df`
          and `df_last` to increase the order of the estimate and/or improve
          the error estimate.
        - Process the function evaluations in a more numerically favorable
          way. For instance, combining the pairs of central difference evals
          into a second-order approximation and using Richardson extrapolation
          to produce a higher order approximation seemed to retain accuracy up
          to very high order.
        - Alternatively, we could use `polyfit` like Jacobi. An advantage of
          fitting polynomial to more points than necessary is improved noise
          tolerance.
        """
        n = work.terms
        n_new = n if work.nit == 0 else 1
        il, ic, io = work.il, work.ic, work.io

        # Central difference
        # `work_fc` is *all* the points at which the function has been evaluated
        # `fc` is the points we're using *this iteration* to produce the estimate
        work_fc = (f[ic][:, :n_new], work.fs[ic], f[ic][:, -n_new:])
        work_fc = xp.concat(work_fc, axis=-1)
        if work.nit == 0:
            fc = work_fc
        else:
            fc = (work_fc[:, :n], work_fc[:, n:n+1], work_fc[:, -n:])
            fc = xp.concat(fc, axis=-1)

        # One-sided difference
        work_fo = xp.concat((work.fs[io], f[io]), axis=-1)
        if work.nit == 0:
            fo = work_fo
        else:
            fo = xp.concat((work_fo[:, 0:1], work_fo[:, -2*n:]), axis=-1)

        work.fs = xp.zeros((ic.shape[0], work.fs.shape[-1] + 2*n_new), dtype=work.dtype)
        work.fs = xpx.at(work.fs)[ic].set(work_fc)
        work.fs = xpx.at(work.fs)[io].set(work_fo)

        wc, wo = _derivative_weights(work, n, xp)
        work.df_last = xp.asarray(work.df, copy=True)
        work.df = xpx.at(work.df)[ic].set(fc @ wc / work.h[ic])
        work.df = xpx.at(work.df)[io].set(fo @ wo / work.h[io])
        work.df = xpx.at(work.df)[il].multiply(-1)

        work.h /= work.fac
        work.error_last = work.error
        # Simple error estimate - the difference in derivative estimates between
        # this iteration and the last. This is typically conservative because if
        # convergence has begin, the true error is much closer to the difference
        # between the current estimate and the *next* error estimate. However,
        # we could use Richarson extrapolation to produce an error estimate that
        # is one order higher, and take the difference between that and
        # `work.df` (which would just be constant factor that depends on `fac`.)
        work.error = xp.abs(work.df - work.df_last)

    def check_termination(work):
        """Terminate due to convergence, non-finite values, or error increase"""
        stop = xp.astype(xp.zeros_like(work.df), xp.bool)

        i = work.error < work.atol + work.rtol*abs(work.df)
        work.status = xpx.at(work.status)[i].set(eim._ECONVERGED)
        stop = xpx.at(stop)[i].set(True)

        if work.nit > 0:
            i = ~((xp.isfinite(work.x) & xp.isfinite(work.df)) | stop)
            work.df = xpx.at(work.df)[i].set(xp.nan)
            work.status = xpx.at(work.status)[i].set(eim._EVALUEERR)
            stop = xpx.at(stop)[i].set(True)

        # With infinite precision, there is a step size below which
        # all smaller step sizes will reduce the error. But in floating point
        # arithmetic, catastrophic cancellation will begin to cause the error
        # to increase again. This heuristic tries to avoid step sizes that are
        # too small. There may be more theoretically sound approaches for
        # detecting a step size that minimizes the total error, but this
        # heuristic seems simple and effective.
        i = (work.error > work.error_last*10) & ~stop
        work.status = xpx.at(work.status)[i].set(_EERRORINCREASE)
        stop = xpx.at(stop)[i].set(True)

        return stop

    def post_termination_check(work):
        return

    def customize_result(res, shape):
        return shape

    return eim._loop(work, callback, shape, maxiter, func, args, dtype,
                     pre_func_eval, post_func_eval, check_termination,
                     post_termination_check, customize_result, res_work_pairs,
                     xp, preserve_shape)

