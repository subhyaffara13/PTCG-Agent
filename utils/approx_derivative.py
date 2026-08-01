
def approx_derivative(fun, x0, method='3-point', rel_step=None, abs_step=None,
                      f0=None, bounds=(-np.inf, np.inf), sparsity=None,
                      as_linear_operator=False, args=(), kwargs=None,
                      full_output=False, workers=None):
    """Compute finite difference approximation of the derivatives of a
    vector-valued function.

    If a function maps from R^n to R^m, its derivatives form m-by-n matrix
    called the Jacobian, where an element (i, j) is a partial derivative of
    f[i] with respect to x[j].

    Parameters
    ----------
    fun : callable
        Function of which to estimate the derivatives. The argument x
        passed to this function is ndarray of shape (n,) (never a scalar
        even if n=1). It must return 1-D array_like of shape (m,) or a scalar.
    x0 : array_like of shape (n,) or float
        Point at which to estimate the derivatives. Float will be converted
        to a 1-D array.
    method : {'3-point', '2-point', 'cs'}, optional
        Finite difference method to use:
            - '2-point' - use the first order accuracy forward or backward
                          difference.
            - '3-point' - use central difference in interior points and the
                          second order accuracy forward or backward difference
                          near the boundary.
            - 'cs' - use a complex-step finite difference scheme. This assumes
                     that the user function is real-valued and can be
                     analytically continued to the complex plane. Otherwise,
                     produces bogus results.
    rel_step : None or array_like, optional
        Relative step size to use. If None (default) the absolute step size is
        computed as ``h = (rel_step * sign(x0) * max(1, abs(x0))).astype(x0.dtype)``,
        with `rel_step` being selected automatically, see Notes. Otherwise
        ``h = (rel_step * sign(x0) * abs(x0)).astype(x0.dtype)``. For
        ``method='3-point'`` the sign of `h` is ignored. The calculated step size
        is possibly adjusted to fit into the bounds.
    abs_step : array_like, optional
        Absolute step size to use, possibly adjusted to fit into the bounds.
        For ``method='3-point'`` the sign of `abs_step` is ignored. By default
        relative steps are used, only if ``abs_step is not None`` are absolute
        steps used. `abs_step` is coerced to the dtype of `x0` during calculation.
    f0 : None or array_like, optional
        If not None it is assumed to be equal to ``fun(x0)``, in this case
        the ``fun(x0)`` is not called. Default is None.
    bounds : tuple of array_like, optional
        Lower and upper bounds on independent variables. Defaults to no bounds.
        Each bound must match the size of `x0` or be a scalar, in the latter
        case the bound will be the same for all variables. Use it to limit the
        range of function evaluation. Bounds checking is not implemented
        when `as_linear_operator` is True.
    sparsity : {None, array_like, sparse array, 2-tuple}, optional
        Defines a sparsity structure of the Jacobian matrix. If the Jacobian
        matrix is known to have only few non-zero elements in each row, then
        it's possible to estimate its several columns by a single function
        evaluation [3]_. To perform such economic computations two ingredients
        are required:

        * structure : array_like or sparse array of shape (m, n). A zero
          element means that a corresponding element of the Jacobian
          identically equals to zero.
        * groups : array_like of shape (n,). A column grouping for a given
          sparsity structure, use `group_columns` to obtain it.

        A single array or a sparse array is interpreted as a sparsity
        structure, and groups are computed inside the function. A tuple is
        interpreted as (structure, groups). If None (default), a standard
        dense differencing will be used.

        Note, that sparse differencing makes sense only for large Jacobian
        matrices where each row contains few non-zero elements.
    as_linear_operator : bool, optional
        When True the function returns an `scipy.sparse.linalg.LinearOperator`.
        Otherwise it returns a dense array or a sparse array depending on
        `sparsity`. The linear operator provides an efficient way of computing
        ``J.dot(p)`` for any vector ``p`` of shape (n,), but does not allow
        direct access to individual elements of the matrix. By default
        `as_linear_operator` is False.
    args, kwargs : tuple and dict, optional
        Additional arguments passed to `fun`. Both empty by default.
        The calling signature is ``fun(x, *args, **kwargs)``.
    full_output : bool, optional
        If True then the function also returns a dictionary with extra information
        about the calculation.
    workers : int or map-like callable, optional
        Supply a map-like callable, such as
        `multiprocessing.Pool.map` for evaluating the population in parallel.
        This evaluation is carried out as ``workers(fun, iterable)``.
        Alternatively, if `workers` is an int the task is subdivided into `workers`
        sections and the fun evaluated in parallel
        (uses `multiprocessing.Pool <multiprocessing>`).
        Supply -1 to use all available CPU cores.
        It is recommended that a map-like be used instead of int, as repeated
        calls to `approx_derivative` will incur large overhead from setting up
        new processes.

    Returns
    -------
    J : {ndarray, sparse array, LinearOperator}
        Finite difference approximation of the Jacobian matrix.
        If `as_linear_operator` is True returns a LinearOperator
        with shape (m, n). Otherwise it returns a dense array or sparse
        array depending on how `sparsity` is defined. If `sparsity`
        is None then an ndarray with shape (m, n) is returned. If
        `sparsity` is not None returns a csr_array or csr_matrix with
        shape (m, n) following the array/matrix type of the incoming structure.
        For sparse arrays and linear operators it is always returned as
        a 2-D structure. For ndarrays, if m=1 it is returned
        as a 1-D gradient array with shape (n,).
        `J.dtype` is the promoted type of ``fun(x0)`` and `x0`.

    info_dict : dict
        Dictionary containing extra information about the calculation. The
        keys include:

        - `nfev`, number of function evaluations. If `as_linear_operator` is True
           then `fun` is expected to track the number of evaluations itself.
           This is because multiple calls may be made to the linear operator which
           are not trackable here.

    See Also
    --------
    check_derivative : Check correctness of a function computing derivatives.

    Notes
    -----
    If `rel_step` is not provided, it is assigned as ``EPS**(1/s)``, where EPS is
    determined from the smallest floating point dtype of `x0` or ``fun(x0)``,
    ``np.finfo(x0.dtype).eps``, s=2 for '2-point' method and
    s=3 for '3-point' method. This relative step approximately minimizes a sum
    of truncation and round-off errors, see [1]_. Relative steps are used by
    default. However, absolute steps are used when ``abs_step is not None``.
    If any of the absolute or relative steps produces an indistinguishable
    difference from the original `x0`, ``(x0 + dx) - x0 == 0``, then a
    automatic step size is substituted for that particular entry.
    The calculated absolute step size, `h`, is coerced to have the same dtype as `x0`.

    The floating point precision of `J` is the promoted type of ``fun(x0)``
    and `x0`. If `rel_step` and `abs_step` are None, then the overall accuracy of
    `J` depends on the smallest floating point dtype of `x0` and ``fun(x0)``,
    as that dtype is used to calculate the default step size.

    A finite difference scheme for '3-point' method is selected automatically.
    The well-known central difference scheme is used for points sufficiently
    far from the boundary, and 3-point forward or backward scheme is used for
    points near the boundary. Both schemes have the second-order accuracy in
    terms of Taylor expansion. Refer to [2]_ for the formulas of 3-point
    forward and backward difference schemes.

    For dense differencing when m=1 Jacobian is returned with a shape (n,),
    on the other hand when n=1 Jacobian is returned with a shape (m, 1).
    Our motivation is the following: a) It handles a case of gradient
    computation (m=1) in a conventional way. b) It clearly separates these two
    different cases. b) In all cases np.atleast_2d can be called to get 2-D
    Jacobian with correct dimensions.

    References
    ----------
    .. [1] W. H. Press et. al. "Numerical Recipes. The Art of Scientific
           Computing. 3rd edition", sec. 5.7.

    .. [2] A. Curtis, M. J. D. Powell, and J. Reid, "On the estimation of
           sparse Jacobian matrices", Journal of the Institute of Mathematics
           and its Applications, 13 (1974), pp. 117-120.

    .. [3] B. Fornberg, "Generation of Finite Difference Formulas on
           Arbitrarily Spaced Grids", Mathematics of Computation 51, 1988.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.optimize._numdiff import approx_derivative
    >>>
    >>> def f(x, c1, c2):
    ...     return np.array([x[0] * np.sin(c1 * x[1]),
    ...                      x[0] * np.cos(c2 * x[1])])
    ...
    >>> x0 = np.array([1.0, 0.5 * np.pi])
    >>> approx_derivative(f, x0, args=(1, 2))
    array([[ 1.,  0.],
           [-1.,  0.]])

    Bounds can be used to limit the region of function evaluation.
    In the example below we compute left and right derivative at point 1.0.

    >>> def g(x):
    ...     return x**2 if x >= 1 else x
    ...
    >>> x0 = 1.0
    >>> approx_derivative(g, x0, bounds=(-np.inf, 1.0))
    array([ 1.])
    >>> approx_derivative(g, x0, bounds=(1.0, np.inf))
    array([ 2.])

    We can also parallelize the derivative calculation using the workers
    keyword.

    >>> from multiprocessing import Pool
    >>> import time
    >>> def fun2(x):       # import from an external file for use with multiprocessing
    ...     time.sleep(0.002)
    ...     return rosen(x)

    >>> rng = np.random.default_rng()
    >>> x0 = rng.uniform(high=10, size=(2000,))
    >>> f0 = rosen(x0)

    >>> %timeit approx_derivative(fun2, x0, f0=f0)     # may vary
    10.5 s ± 5.91 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    >>> elapsed = []
    >>> with Pool() as workers:
    ...     for i in range(10):
    ...         t = time.perf_counter()
    ...         approx_derivative(fun2, x0, workers=workers.map, f0=f0)
    ...         et = time.perf_counter()
    ...         elapsed.append(et - t)
    >>> np.mean(elapsed)    # may vary
    np.float64(1.442545195999901)

    Create a map-like vectorized version. `x` is a generator, so first of all
    a 2-D array, `xx`, is reconstituted. Here `xx` has shape `(Y, N)` where `Y`
    is the number of function evaluations to perform and `N` is the dimensionality
    of the objective function. The underlying objective function is `rosen`, which
    requires `xx` to have shape `(N, Y)`, so a transpose is required.

    >>> def fun(f, x, *args, **kwds):
    ...     xx = np.r_[[xs for xs in x]]
    ...     return f(xx.T)
    >>> %timeit approx_derivative(fun2, x0, workers=fun, f0=f0)    # may vary
    91.8 ms ± 755 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)

    """
    if method not in ['2-point', '3-point', 'cs']:
        raise ValueError(f"Unknown method '{method}'. ")

    info_dict = {'nfev': None}

    xp = array_namespace(x0)
    _x = xpx.atleast_nd(xp.asarray(x0), ndim=1, xp=xp)
    _dtype = xp.float64
    if xp.isdtype(_x.dtype, "real floating"):
        _dtype = _x.dtype

    # promotes to floating
    x0 = xp.astype(_x, _dtype)

    if x0.ndim > 1:
        raise ValueError("`x0` must have at most 1 dimension.")

    lb, ub = _prepare_bounds(bounds, x0)

    if lb.shape != x0.shape or ub.shape != x0.shape:
        raise ValueError("Inconsistent shapes between bounds and `x0`.")

    if as_linear_operator and not (np.all(np.isinf(lb))
                                   and np.all(np.isinf(ub))):
        raise ValueError("Bounds not supported when "
                         "`as_linear_operator` is True.")

    if kwargs is None:
        kwargs = {}

    fun_wrapped = _Fun_Wrapper(fun, x0, args, kwargs)

    # Record how function evaluations are consumed by `approx_derivative`.
    # Historically this was done by upstream functions wrapping `fun`.
    # However, with parallelization via workers it was going to be impossible to
    # keep that counter updated across Processes. Counter synchronisation can
    # be achieved via multiprocessing.Value and a Pool. However, workers can be
    # any map-like, not necessarily a Pool, so initialization of the Value would
    # be difficult.
    nfev = _nfev = 0

    if f0 is None:
        f0 = fun_wrapped(x0)
        nfev = 1
    else:
        f0 = np.atleast_1d(f0)
        if f0.ndim > 1:
            raise ValueError("`f0` passed has more than 1 dimension.")

    if np.any((x0 < lb) | (x0 > ub)):
        raise ValueError("`x0` violates bound constraints.")

    if as_linear_operator:
        if rel_step is None:
            rel_step = _eps_for_method(x0.dtype, f0.dtype, method)

        J, _ = _linear_operator_difference(fun_wrapped, x0,
                                           f0, rel_step, method)
    else:
        # by default we use rel_step
        if abs_step is None:
            h = _compute_absolute_step(rel_step, x0, f0, method)
        else:
            # user specifies an absolute step
            sign_x0 = (x0 >= 0).astype(x0.dtype) * 2 - 1
            h = abs_step

            # cannot have a zero step. This might happen if x0 is very large
            # or small. In which case fall back to relative step.
            dx = ((x0 + h) - x0)
            h = np.where(dx == 0,
                         _eps_for_method(x0.dtype, f0.dtype, method) *
                         sign_x0 * np.maximum(1.0, np.abs(x0)),
                         h)
            h = h.astype(x0.dtype)

        if method == '2-point':
            h, use_one_sided = _adjust_scheme_to_bounds(
                x0, h, 1, '1-sided', lb, ub)
        elif method == '3-point':
            h, use_one_sided = _adjust_scheme_to_bounds(
                x0, h, 1, '2-sided', lb, ub)
        elif method == 'cs':
            use_one_sided = False

        # normalize workers
        workers = workers or map
        with MapWrapper(workers) as mf:
            if sparsity is None:
                J, _nfev = _dense_difference(fun_wrapped, x0, f0, h,
                                         use_one_sided, method,
                                         mf)
            else:
                if not issparse(sparsity) and len(sparsity) == 2:
                    structure, groups = sparsity
                else:
                    structure = sparsity
                    groups = group_columns(sparsity)

                if issparse(structure):
                    structure = structure.tocsc()
                else:
                    structure = np.atleast_2d(structure)
                groups = np.atleast_1d(groups)
                J, _nfev = _sparse_difference(fun_wrapped, x0, f0, h,
                                             use_one_sided, structure,
                                             groups, method, mf)

    if full_output:
        nfev += _nfev
        info_dict["nfev"] = nfev
        return J, info_dict
    else:
        return J

