
def boxcox_normmax(
    x, brack=None, method='pearsonr', optimizer=None, *, ymax=_BigFloat_singleton,
    nan_policy='propagate'
):
    """Compute optimal Box-Cox transform parameter for input data.

    Parameters
    ----------
    x : array_like
        Input array. All entries must be positive, finite, real numbers.
    brack : 2-tuple, optional, default (-2.0, 2.0)
         The starting interval for a downhill bracket search for the default
         `optimize.brent` solver. Note that this is in most cases not
         critical; the final result is allowed to be outside this bracket.
         If `optimizer` is passed, `brack` must be None.
    method : str, optional
        The method to determine the optimal transform parameter (`boxcox`
        ``lmbda`` parameter). Options are:

        'pearsonr'  (default)
            Maximizes the Pearson correlation coefficient between
            ``y = boxcox(x)`` and the expected values for ``y`` if `x` would be
            normally-distributed.

        'mle'
            Maximizes the log-likelihood `boxcox_llf`.  This is the method used
            in `boxcox`.

        'all'
            Use all optimization methods available, and return all results.
            Useful to compare different methods.
    optimizer : callable, optional
        `optimizer` is a callable that accepts one argument:

        fun : callable
            The objective function to be minimized. `fun` accepts one argument,
            the Box-Cox transform parameter `lmbda`, and returns the value of
            the function (e.g., the negative log-likelihood) at the provided
            argument. The job of `optimizer` is to find the value of `lmbda`
            that *minimizes* `fun`.

        and returns an object, such as an instance of
        `scipy.optimize.OptimizeResult`, which holds the optimal value of
        `lmbda` in an attribute `x`.

        See the example below or the documentation of
        `scipy.optimize.minimize_scalar` for more information.
    ymax : float, optional
        The unconstrained optimal transform parameter may cause Box-Cox
        transformed data to have extreme magnitude or even overflow.
        This parameter constrains MLE optimization such that the magnitude
        of the transformed `x` does not exceed `ymax`. The default is
        the maximum value of the input dtype. If set to infinity,
        `boxcox_normmax` returns the unconstrained optimal lambda.
        Ignored when ``method='pearsonr'``.
    nan_policy : {'propagate', 'omit', 'raise'}
        Defines how to handle input NaNs.

        - ``propagate``: if a NaN is present in the input, the output will be NaN.
        - ``omit``: NaNs will be omitted when performing the calculation.
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

    Returns
    -------
    maxlog : float or ndarray
        The optimal transform parameter found.  An array instead of a scalar
        for ``method='all'``.

    See Also
    --------
    boxcox, boxcox_llf, boxcox_normplot, scipy.optimize.minimize_scalar

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    We can generate some data and determine the optimal ``lmbda`` in various
    ways:

    >>> rng = np.random.default_rng()
    >>> x = stats.loggamma.rvs(5, size=30, random_state=rng) + 5
    >>> y, lmax_mle = stats.boxcox(x)
    >>> lmax_pearsonr = stats.boxcox_normmax(x)

    >>> lmax_mle
    2.217563431465757
    >>> lmax_pearsonr
    2.238318660200961
    >>> stats.boxcox_normmax(x, method='all')
    array([2.23831866, 2.21756343])

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> prob = stats.boxcox_normplot(x, -10, 10, plot=ax)
    >>> ax.axvline(lmax_mle, color='r')
    >>> ax.axvline(lmax_pearsonr, color='g', ls='--')

    >>> plt.show()

    Alternatively, we can define our own `optimizer` function. Suppose we
    are only interested in values of `lmbda` on the interval [6, 7], we
    want to use `scipy.optimize.minimize_scalar` with ``method='bounded'``,
    and we want to use tighter tolerances when optimizing the log-likelihood
    function. To do this, we define a function that accepts positional argument
    `fun` and uses `scipy.optimize.minimize_scalar` to minimize `fun` subject
    to the provided bounds and tolerances:

    >>> from scipy import optimize
    >>> options = {'xatol': 1e-12}  # absolute tolerance on `x`
    >>> def optimizer(fun):
    ...     return optimize.minimize_scalar(fun, bounds=(6, 7),
    ...                                     method="bounded", options=options)
    >>> stats.boxcox_normmax(x, optimizer=optimizer)
    6.000000000
    """
    x = np.asarray(x)

    contains_nan = _contains_nan(x, nan_policy, xp_omit_okay=True)
    if contains_nan:
        if nan_policy == 'propagate':
            NaN = _get_nan(x, xp=np)[()]
            return np.asarray([NaN, NaN]) if method == 'all' else NaN
        x = x[~np.isnan(x)]  # `nan_policy='omit

    if not np.all(np.isfinite(x) & (x >= 0)):
        message = ("The `x` argument of `boxcox_normmax` must contain "
                   "only positive, finite, real numbers.")
        raise ValueError(message)

    end_msg = "exceed specified `ymax`."
    if ymax is _BigFloat_singleton:
        dtype = x.dtype if np.issubdtype(x.dtype, np.floating) else np.float64
        # 10000 is a safety factor because `special.boxcox` overflows prematurely.
        ymax = np.finfo(dtype).max / 10000
        end_msg = f"overflow in {dtype}."
    elif ymax <= 0:
        raise ValueError("`ymax` must be strictly positive")

    # If optimizer is not given, define default 'brent' optimizer.
    if optimizer is None:

        # Set default value for `brack`.
        if brack is None:
            brack = (-2.0, 2.0)

        def _optimizer(func, args):
            return optimize.brent(func, args=args, brack=brack)

    # Otherwise check optimizer.
    else:
        if not callable(optimizer):
            raise ValueError("`optimizer` must be a callable")

        if brack is not None:
            raise ValueError("`brack` must be None if `optimizer` is given")

        # `optimizer` is expected to return a `OptimizeResult` object, we here
        # get the solution to the optimization problem.
        def _optimizer(func, args):
            def func_wrapped(x):
                return func(x, *args)
            return getattr(optimizer(func_wrapped), 'x', None)

    def _pearsonr(x):
        osm_uniform = _calc_uniform_order_statistic_medians(len(x))
        xvals = distributions.norm.ppf(osm_uniform)

        def _eval_pearsonr(lmbda, xvals, samps):
            # This function computes the x-axis values of the probability plot
            # and computes a linear regression (including the correlation) and
            # returns ``1 - r`` so that a minimization function maximizes the
            # correlation.
            y = boxcox(samps, lmbda)
            yvals = np.sort(y)
            r, prob = _stats_py.pearsonr(xvals, yvals)
            return 1 - r

        return _optimizer(_eval_pearsonr, args=(xvals, x))

    def _mle(x):
        def _eval_mle(lmb, data):
            # function to minimize
            return -boxcox_llf(lmb, data)

        return _optimizer(_eval_mle, args=(x,))

    def _all(x):
        maxlog = np.empty(2, dtype=float)
        maxlog[0] = _pearsonr(x)
        maxlog[1] = _mle(x)
        return maxlog

    methods = {'pearsonr': _pearsonr,
               'mle': _mle,
               'all': _all}
    if method not in methods.keys():
        raise ValueError(f"Method {method} not recognized.")

    optimfunc = methods[method]

    res = optimfunc(x)

    if res is None:
        message = ("The `optimizer` argument of `boxcox_normmax` must return "
                   "an object containing the optimal `lmbda` in attribute `x`.")
        raise ValueError(message)
    elif not np.isinf(ymax):  # adjust the final lambda
        # x > 1, boxcox(x) > 0; x < 1, boxcox(x) < 0
        xmax, xmin = np.max(x), np.min(x)
        if xmin >= 1:
            x_treme = xmax
        elif xmax <= 1:
            x_treme = xmin
        else:  # xmin < 1 < xmax
            indicator = special.boxcox(xmax, res) > abs(special.boxcox(xmin, res))
            if isinstance(res, np.ndarray):
                indicator = indicator[1]  # select corresponds with 'mle'
            x_treme = xmax if indicator else xmin

        mask = abs(special.boxcox(x_treme, res)) > ymax
        if np.any(mask):
            message = (
                f"The optimal lambda is {res}, but the returned lambda is the "
                f"constrained optimum to ensure that the maximum or the minimum "
                f"of the transformed data does not " + end_msg
            )
            warnings.warn(message, stacklevel=2)

            # Return the constrained lambda to ensure the transformation
            # does not cause overflow or exceed specified `ymax`
            constrained_res = _boxcox_inv_lmbda(x_treme, ymax * np.sign(x_treme - 1))

            if isinstance(res, np.ndarray):
                res[mask] = constrained_res
            else:
                res = constrained_res
    return res

