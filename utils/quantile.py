
def quantile(
    a: ArrayLike,
    q: ArrayLike,
    axis: AxisLike = None,
    out: OutArray | None = None,
    overwrite_input=False,
    method="linear",
    keepdims: KeepDims = False,
    *,
    interpolation: NotImplementedType = None,
):
    if overwrite_input:
        # raise NotImplementedError("overwrite_input in quantile not implemented.")
        # NumPy documents that `overwrite_input` MAY modify inputs:
        # https://numpy.org/doc/stable/reference/generated/numpy.percentile.html#numpy-percentile
        # Here we choose to work out-of-place because why not.
        pass

    if not a.dtype.is_floating_point:
        dtype = _dtypes_impl.default_dtypes().float_dtype
        a = a.to(dtype)

    # edge case: torch.quantile only supports float32 and float64
    if a.dtype == torch.float16:
        a = a.to(torch.float32)

    if axis is None:
        a = a.flatten()
        q = q.flatten()
        axis = (0,)
    else:
        axis = _util.normalize_axis_tuple(axis, a.ndim)

    # FIXME(Mario) Doesn't np.quantile accept a tuple?
    # torch.quantile does accept a number. If we don't want to implement the tuple behaviour
    # (it's deffo low prio) change `normalize_axis_tuple` into a normalize_axis index above.
    axis = _util.allow_only_single_axis(axis)

    q = _util.cast_if_needed(q, a.dtype)

    return torch.quantile(a, q, axis=axis, interpolation=method)


def quantile(expr, evaluate=True, **kwargs):
    r"""
    Return the :math:`p^{th}` order quantile of a probability distribution.

    Explanation
    ===========

    Quantile is defined as the value at which the probability of the random
    variable is less than or equal to the given probability.

    .. math::
        Q(p) = \inf\{x \in (-\infty, \infty) : p \le F(x)\}

    Examples
    ========

    >>> from sympy.stats import quantile, Die, Exponential
    >>> from sympy import Symbol, pprint
    >>> p = Symbol("p")

    >>> l = Symbol("lambda", positive=True)
    >>> X = Exponential("x", l)
    >>> quantile(X)(p)
    -log(1 - p)/lambda

    >>> D = Die("d", 6)
    >>> pprint(quantile(D)(p), use_unicode=False)
    /nan  for Or(p > 1, p < 0)
    |
    | 1       for p <= 1/6
    |
    | 2       for p <= 1/3
    |
    < 3       for p <= 1/2
    |
    | 4       for p <= 2/3
    |
    | 5       for p <= 5/6
    |
    \ 6        for p <= 1

    """
    result = pspace(expr).compute_quantile(expr, **kwargs)

    if evaluate and hasattr(result, 'doit'):
        return result.doit()
    else:
        return result


def quantile(x, p, *, method='linear', axis=0, nan_policy='propagate', keepdims=None,
             weights=None):
    """
    Compute the p-th quantile of the data along the specified axis.

    Parameters
    ----------
    x : array_like of real numbers
        Data array.
    p : array_like of float
        Probability or sequence of probabilities of the quantiles to compute.
        Values must be between 0 and 1 (inclusive).
        While `numpy.quantile` can only compute quantiles according to the Cartesian
        product of the first two arguments, this function enables calculation of
        quantiles at different probabilities for each axis slice by following
        broadcasting rules like those of `scipy.stats` reducing functions.
        See `axis`, `keepdims`, and the examples.
    method : str, default: 'linear'
        The method to use for estimating the quantile.
        The available options, numbered as they appear in [1]_, are:

        1. 'inverted_cdf'
        2. 'averaged_inverted_cdf'
        3. 'closest_observation'
        4. 'interpolated_inverted_cdf'
        5. 'hazen'
        6. 'weibull'
        7. 'linear'  (default)
        8. 'median_unbiased'
        9. 'normal_unbiased'

        'harrell-davis' is also available to compute the quantile estimate
        according to [2]_.

        'round_outward', 'round_inward', and 'round_nearest' are available for use
        in trimming and winsorizing data.

        See Notes for details.
    axis : int or None, default: 0
        Axis along which the quantiles are computed.
        ``None`` ravels both `x` and `p` before performing the calculation,
        without checking whether the original shapes were compatible.
        As in other `scipy.stats` functions, a positive integer `axis` is resolved
        after prepending 1s to the shape of `x` or `p` as needed until the two arrays
        have the same dimensionality. When providing `x` and `p` with different
        dimensionality, consider using negative `axis` integers for clarity.
    nan_policy : str, default: 'propagate'
        Defines how to handle NaNs in the input data `x`.

        - ``propagate``: if a NaN is present in the axis slice (e.g. row) along
          which the  statistic is computed, the corresponding slice of the output
          will contain NaN(s).
        - ``omit``: NaNs will be omitted when performing the calculation.
          If insufficient data remains in the axis slice along which the
          statistic is computed, the corresponding slice of the output will
          contain NaN(s).
        - ``raise``: if a NaN is present, a ``ValueError`` will be raised.

        If NaNs are present in `p`, a ``ValueError`` will be raised.
    keepdims : bool, optional
        Consider the case in which `x` is 1-D and `p` is a scalar: the quantile
        is a reducing statistic, and the default behavior is to return a scalar.
        If `keepdims` is set to True, the axis will not be reduced away, and the
        result will be a 1-D array with one element.

        The general case is more subtle, since multiple quantiles may be
        requested for each axis-slice of `x`. For instance, if both `x` and `p`
        are 1-D and ``p.size > 1``, no axis can be reduced away; there must be an
        axis to contain the number of quantiles given by ``p.size``. Therefore:

        - By default, the axis will be reduced away if possible (i.e. if there is
          exactly one element of `p` per axis-slice of `x`).
        - If `keepdims` is set to True, the axis will not be reduced away.
        - If `keepdims` is set to False, the axis will be reduced away
          if possible, and an error will be raised otherwise.

    weights : array_like of finite, non-negative real numbers
        Frequency weights; e.g., for counting number weights,
        ``quantile(x, p, weights=weights)`` is equivalent to
        ``quantile(np.repeat(x, weights), p)``. Values other than finite counting
        numbers are accepted, but may not have valid statistical interpretations.
        Not compatible with ``method='harrell-davis'`` or those that begin with
        ``'round_'``.

    Returns
    -------
    quantile : scalar or ndarray
        The resulting quantile(s). The dtype is the result dtype of `x` and `p`.

    See Also
    --------
    numpy.quantile
    estimated_cdf
    :ref:`outliers`

    Notes
    -----
    Given a sample `x` from an underlying distribution, `quantile` provides a
    nonparametric estimate of the inverse cumulative distribution function.

    By default, this is done by interpolating between adjacent elements in
    ``y``, a sorted copy of `x`::

        (1-g)*y[j] + g*y[j+1]

    where the index ``j`` and coefficient ``g`` are the integral and
    fractional components of ``p * (n-1)``, and ``n`` is the number of
    elements in the sample.

    This is a special case of Equation 1 of H&F [1]_. More generally,

    - ``j = (p*n + m - 1) // 1``, and
    - ``g = (p*n + m - 1) % 1``,

    where ``m`` may be defined according to several different conventions.
    The preferred convention may be selected using the ``method`` parameter:

    =============================== =============== ===============
    ``method``                      number in H&F   ``m``
    =============================== =============== ===============
    ``interpolated_inverted_cdf``   4               ``0``
    ``hazen``                       5               ``1/2``
    ``weibull``                     6               ``p``
    ``linear`` (default)            7               ``1 - p``
    ``median_unbiased``             8               ``p/3 + 1/3``
    ``normal_unbiased``             9               ``p/4 + 3/8``
    =============================== =============== ===============

    Note that indices ``j`` and ``j + 1`` are clipped to the range ``0`` to
    ``n - 1`` when the results of the formula would be outside the allowed
    range of non-negative indices. When ``j`` is clipped to zero, ``g`` is
    set to zero as well. The ``-1`` in the formulas for ``j`` and ``g``
    accounts for Python's 0-based indexing.

    The table above includes only the estimators from [1]_ that are continuous
    functions of probability `p` (estimators 4-9). SciPy also provides the
    three discontinuous estimators from [1]_ (estimators 1-3), where ``j`` is
    defined as above, ``m`` is defined as follows, and ``g`` is ``0`` when
    ``index = p*n + m - 1`` is less than ``0`` and otherwise is defined below.

    1. ``inverted_cdf``: ``m = 0`` and ``g = int(index - j > 0)``
    2. ``averaged_inverted_cdf``: ``m = 0`` and
       ``g = (1 + int(index - j > 0)) / 2``
    3. ``closest_observation``: ``m = -1/2`` and
       ``g = 1 - int((index == j) & (j%2 == 1))``

    Note that for methods ``inverted_cdf`` and ``averaged_inverted_cdf``, only the
    relative proportions of tied observations (and relative weights) affect the
    results; for all other methods, the total number of observations (and absolute
    weights) matter.

    A different strategy for computing quantiles from [2]_, ``method='harrell-davis'``,
    uses a weighted combination of all elements. The weights are computed as:

    .. math::

        w_{n, i} = I_{i/n}(a, b) - I_{(i - 1)/n}(a, b)

    where :math:`n` is the number of elements in the sample,
    :math:`i` are the indices :math:`1, 2, ..., n-1, n` of the sorted elements,
    :math:`a = p (n + 1)`, :math:`b = (1 - p)(n + 1)`,
    :math:`p` is the probability of the quantile, and
    :math:`I` is the regularized, lower incomplete beta function
    (`scipy.special.betainc`).

    ``method='round_nearest'`` is equivalent to indexing ``y[j]``, where::

        j = int(np.round(p*n) if p < 0.5 else np.round(n*p - 1))

    This is useful when winsorizing data: replacing ``p*n`` of the most extreme
    observations with the next most extreme observation. ``method='round_outward'``
    adjusts the direction of rounding to winsorize fewer elements::

        j = int(np.floor(p*n) if p < 0.5 else np.ceil(n*p - 1))

    and ``method='round_inward'`` rounds to winsorize more elements::

        j = int(np.ceil(p*n) if p < 0.5 else np.floor(n*p - 1))

    These methods are also useful for trimming data: removing ``p*n`` of the most
    extreme observations. See :ref:`outliers` for example applications.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> x = np.asarray([[10, 8, 7, 5, 4],
    ...                 [0, 1, 2, 3, 5]])

    Take the median of each row.

    >>> stats.quantile(x, 0.5, axis=-1)
    array([7.,  2.])

    Take a different quantile for each row.

    >>> stats.quantile(x, [[0.25], [0.75]], axis=-1, keepdims=True)
    array([[5.],
           [3.]])

    Take multiple quantiles for each row.

    >>> stats.quantile(x, [0.25, 0.75], axis=-1)
    array([[5., 8.],
           [1., 3.]])

    Take different quantiles for each row.

    >>> p = np.asarray([[0.25, 0.75],
    ...                 [0.5, 1.0]])
    >>> stats.quantile(x, p, axis=-1)
    array([[5., 8.],
           [2., 5.]])

    Take different quantiles for each column.

    >>> stats.quantile(x.T, p.T, axis=0)
    array([[5., 2.],
           [8., 5.]])

    References
    ----------
    .. [1] R. J. Hyndman and Y. Fan,
       "Sample quantiles in statistical packages,"
       The American Statistician, 50(4), pp. 361-365, 1996
    .. [2] Harrell, Frank E., and C. E. Davis.
       "A new distribution-free quantile estimator."
       Biometrika 69.3 (1982): 635-640.

    """
    # Input validation / standardization

    temp = _quantile_iv(x, p, method, axis, nan_policy, keepdims, weights)
    (y, p, method, axis, nan_policy, keepdims,
     n, axis_none, ndim, p_mask, weights, xp) = temp

    if method in {'inverted_cdf', 'averaged_inverted_cdf', 'closest_observation',
                  'hazen', 'interpolated_inverted_cdf', 'linear',
                  'median_unbiased', 'normal_unbiased', 'weibull'}:
        res = _quantile_hf(y, p, n, method, weights, xp)
    elif method in {'harrell-davis'}:
        res = _quantile_hd(y, p, n, xp)
    elif method in {'_lower', '_midpoint', '_higher', '_nearest'}:
        res = _quantile_bc(y, p, n, method, xp)
    else:  # method.startswith('round'):
        res = _quantile_winsor(y, p, n, method, xp)

    return _post_quantile(res, p_mask, axis, axis_none, ndim, keepdims, xp)


def quantile(a,
             q,
             axis=None,
             out=None,
             overwrite_input=False,
             method="linear",
             keepdims=False,
             *,
             weights=None):
    """
    Compute the q-th quantile of the data along the specified axis.

    Parameters
    ----------
    a : array_like of real numbers
        Input array or object that can be converted to an array.
    q : array_like of float
        Probability or sequence of probabilities of the quantiles to compute.
        Values must be between 0 and 1 inclusive.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the quantiles are computed. The default is
        to compute the quantile(s) along a flattened version of the array.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape and buffer length as the expected output, but the
        type (of the output) will be cast if necessary.
    overwrite_input : bool, optional
        If True, then allow the input array `a` to be modified by
        intermediate calculations, to save memory. In this case, the
        contents of the input `a` after this function completes is
        undefined.
    method : str, optional
        This parameter specifies the method to use for estimating the
        quantile.  There are many different methods, some unique to NumPy.
        The recommended options, numbered as they appear in [1]_, are:

        1. 'inverted_cdf'
        2. 'averaged_inverted_cdf'
        3. 'closest_observation'
        4. 'interpolated_inverted_cdf'
        5. 'hazen'
        6. 'weibull'
        7. 'linear'  (default)
        8. 'median_unbiased'
        9. 'normal_unbiased'

        The first three methods are discontinuous. For backward compatibility
        with previous versions of NumPy, the following discontinuous variations
        of the default 'linear' (7.) option are available:

        * 'lower'
        * 'higher',
        * 'midpoint'
        * 'nearest'

        See Notes for details.

        .. versionchanged:: 1.22.0
            This argument was previously called "interpolation" and only
            offered the "linear" default and last four options.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left in
        the result as dimensions with size one. With this option, the
        result will broadcast correctly against the original array `a`.

    weights : array_like, optional
        An array of weights associated with the values in `a`. Each value in
        `a` contributes to the quantile according to its associated weight.
        The weights array can either be 1-D (in which case its length must be
        the size of `a` along the given axis) or of the same shape as `a`.
        If `weights=None`, then all data in `a` are assumed to have a
        weight equal to one.
        Only `method="inverted_cdf"` supports weights.
        See the notes for more details.

        .. versionadded:: 2.0.0

    Returns
    -------
    quantile : scalar or ndarray
        If `q` is a single probability and `axis=None`, then the result
        is a scalar. If multiple probability levels are given, first axis
        of the result corresponds to the quantiles. The other axes are
        the axes that remain after the reduction of `a`. If the input
        contains integers or floats smaller than ``float64``, the output
        data-type is ``float64``. Otherwise, the output data-type is the
        same as that of the input. If `out` is specified, that array is
        returned instead.

    See Also
    --------
    mean
    percentile : equivalent to quantile, but with q in the range [0, 100].
    median : equivalent to ``quantile(..., 0.5)``
    nanquantile

    Notes
    -----
    Given a sample `a` from an underlying distribution, `quantile` provides a
    nonparametric estimate of the inverse cumulative distribution function.

    By default, this is done by interpolating between adjacent elements in
    ``y``, a sorted copy of `a`::

        (1-g)*y[j] + g*y[j+1]

    where the index ``j`` and coefficient ``g`` are the integral and
    fractional components of ``q * (n-1)``, and ``n`` is the number of
    elements in the sample.

    This is a special case of Equation 1 of H&F [1]_. More generally,

    - ``j = (q*n + m - 1) // 1``, and
    - ``g = (q*n + m - 1) % 1``,

    where ``m`` may be defined according to several different conventions.
    The preferred convention may be selected using the ``method`` parameter:

    =============================== =============== ===============
    ``method``                      number in H&F   ``m``
    =============================== =============== ===============
    ``interpolated_inverted_cdf``   4               ``0``
    ``hazen``                       5               ``1/2``
    ``weibull``                     6               ``q``
    ``linear`` (default)            7               ``1 - q``
    ``median_unbiased``             8               ``q/3 + 1/3``
    ``normal_unbiased``             9               ``q/4 + 3/8``
    =============================== =============== ===============

    Note that indices ``j`` and ``j + 1`` are clipped to the range ``0`` to
    ``n - 1`` when the results of the formula would be outside the allowed
    range of non-negative indices. The ``- 1`` in the formulas for ``j`` and
    ``g`` accounts for Python's 0-based indexing.

    The table above includes only the estimators from H&F that are continuous
    functions of probability `q` (estimators 4-9). NumPy also provides the
    three discontinuous estimators from H&F (estimators 1-3), where ``j`` is
    defined as above, ``m`` is defined as follows, and ``g`` is a function
    of the real-valued ``index = q*n + m - 1`` and ``j``.

    1. ``inverted_cdf``: ``m = 0`` and ``g = int(index - j > 0)``
    2. ``averaged_inverted_cdf``: ``m = 0`` and
       ``g = (1 + int(index - j > 0)) / 2``
    3. ``closest_observation``: ``m = -1/2`` and
       ``g = 1 - int((index == j) & (j%2 == 1))``

    For backward compatibility with previous versions of NumPy, `quantile`
    provides four additional discontinuous estimators. Like
    ``method='linear'``, all have ``m = 1 - q`` so that ``j = q*(n-1) // 1``,
    but ``g`` is defined as follows.

    - ``lower``: ``g = 0``
    - ``midpoint``: ``g = 0.5``
    - ``higher``: ``g = 1``
    - ``nearest``: ``g = (q*(n-1) % 1) > 0.5``

    **Weighted quantiles:**
    More formally, the quantile at probability level :math:`q` of a cumulative
    distribution function :math:`F(y)=P(Y \\leq y)` with probability measure
    :math:`P` is defined as any number :math:`x` that fulfills the
    *coverage conditions*

    .. math:: P(Y < x) \\leq q \\quad\\text{and}\\quad P(Y \\leq x) \\geq q

    with random variable :math:`Y\\sim P`.
    Sample quantiles, the result of `quantile`, provide nonparametric
    estimation of the underlying population counterparts, represented by the
    unknown :math:`F`, given a data vector `a` of length ``n``.

    Some of the estimators above arise when one considers :math:`F` as the
    empirical distribution function of the data, i.e.
    :math:`F(y) = \\frac{1}{n} \\sum_i 1_{a_i \\leq y}`.
    Then, different methods correspond to different choices of :math:`x` that
    fulfill the above coverage conditions. Methods that follow this approach
    are ``inverted_cdf`` and ``averaged_inverted_cdf``.

    For weighted quantiles, the coverage conditions still hold. The
    empirical cumulative distribution is simply replaced by its weighted
    version, i.e.
    :math:`P(Y \\leq t) = \\frac{1}{\\sum_i w_i} \\sum_i w_i 1_{x_i \\leq t}`.
    Only ``method="inverted_cdf"`` supports weights.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[10, 7, 4], [3, 2, 1]])
    >>> a
    array([[10,  7,  4],
           [ 3,  2,  1]])
    >>> np.quantile(a, 0.5)
    3.5
    >>> np.quantile(a, 0.5, axis=0)
    array([6.5, 4.5, 2.5])
    >>> np.quantile(a, 0.5, axis=1)
    array([7.,  2.])
    >>> np.quantile(a, 0.5, axis=1, keepdims=True)
    array([[7.],
           [2.]])
    >>> m = np.quantile(a, 0.5, axis=0)
    >>> out = np.zeros_like(m)
    >>> np.quantile(a, 0.5, axis=0, out=out)
    array([6.5, 4.5, 2.5])
    >>> m
    array([6.5, 4.5, 2.5])
    >>> b = a.copy()
    >>> np.quantile(b, 0.5, axis=1, overwrite_input=True)
    array([7.,  2.])
    >>> assert not np.all(a == b)

    See also `numpy.percentile` for a visualization of most methods.

    References
    ----------
    .. [1] R. J. Hyndman and Y. Fan,
       "Sample quantiles in statistical packages,"
       The American Statistician, 50(4), pp. 361-365, 1996

    """
    a = np.asanyarray(a)
    if a.dtype.kind == "c":
        raise TypeError("a must be an array of real numbers")

    weak_q = type(q) in (int, float)  # use weak promotion for final result type
    q = np.asanyarray(q)

    if not _quantile_is_valid(q):
        raise ValueError("Quantiles must be in the range [0, 1]")

    if weights is not None:
        if method != "inverted_cdf":
            msg = ("Only method 'inverted_cdf' supports weights. "
                   f"Got: {method}.")
            raise ValueError(msg)
        if axis is not None:
            axis = _nx.normalize_axis_tuple(axis, a.ndim, argname="axis")
        weights = _weights_are_valid(weights=weights, a=a, axis=axis)
        if np.any(weights < 0):
            raise ValueError("Weights must be non-negative.")

    return _quantile_unchecked(
        a, q, axis, out, overwrite_input, method, keepdims, weights, weak_q)


def quantile(a: ArrayLike, q: ArrayLike, axis: int | tuple[int, ...] | None = None,
             out: None = None, overwrite_input: bool = False, method: str = "linear",
             keepdims: bool = False, *, weights: ArrayLike | None = None) -> Array:
  """Compute the quantile of the data along the specified axis.

  JAX implementation of :func:`numpy.quantile`.

  Args:
    a: N-dimensional array input.
    q: scalar or 1-dimensional array specifying the desired quantiles. ``q``
      should contain floating-point values between ``0.0`` and ``1.0``.
    axis: optional axis or tuple of axes along which to compute the quantile
    out: not implemented by JAX; will error if not None
    overwrite_input: not implemented by JAX; will error if not False
    method: specify the interpolation method to use. Options are one of
      ``["linear", "lower", "higher", "midpoint", "nearest"]``.
      default is ``linear``.
    keepdims: if True, then the returned array will have the same number of
      dimensions as the input. Default is False.
    weights: keyword-only. optional array of weights associated with the values in ``a``.
      Each value in ``a`` contributes to the quantile according to its
      associated weight. The weights array must be broadcastable to the same
      shape as ``a``. Only works with ``method="inverted_cdf"``.

  Returns:
    An array containing the specified quantiles along the specified axes.

  See also:
    - :func:`jax.numpy.nanquantile`: compute the quantile while ignoring NaNs
    - :func:`jax.numpy.percentile`: compute the percentile (0-100)

  Examples:
    Computing the median and quartiles of an array, with linear interpolation:

    >>> x = jnp.arange(10)
    >>> q = jnp.array([0.25, 0.5, 0.75])
    >>> jnp.quantile(x, q)
    Array([2.25, 4.5 , 6.75], dtype=float32)

    Computing the quartiles using nearest-value interpolation:

    >>> jnp.quantile(x, q, method='nearest')
    Array([2., 4., 7.], dtype=float32)

    Computing weighted quantiles:

    >>> x = jnp.array([1, 2, 3, 4, 5])
    >>> weights = jnp.array([1, 1, 2, 1, 1])
    >>> jnp.quantile(x, 0.5, weights=weights, method='inverted_cdf')
    Array(3., dtype=float32)
  """
  a, q = ensure_arraylike("quantile", a, q)
  if weights is not None:
    weights = ensure_arraylike("quantile", weights)
  if overwrite_input or out is not None:
    raise ValueError("jax.numpy.quantile does not support overwrite_input=True "
                     "or out != None")
  return _quantile(a, q, axis, method, keepdims, False, weights)

