
def pmean(xs, axis_name):
  warnings.warn('use jax.lax.pmean instead', DeprecationWarning)
  return lax.pmean(xs, axis_name)


def pmean(a, p, *, axis=0, dtype=None, weights=None):
    r"""Calculate the weighted power mean along the specified axis.

    The weighted power mean of the array :math:`a_i` associated to weights
    :math:`w_i` is:

    .. math::

        \left( \frac{ \sum_{i=1}^n w_i a_i^p }{ \sum_{i=1}^n w_i }
              \right)^{ 1 / p } \, ,

    and, with equal weights, it gives:

    .. math::

        \left( \frac{ 1 }{ n } \sum_{i=1}^n a_i^p \right)^{ 1 / p }  \, .

    When ``p=0``, it returns the geometric mean.

    This mean is also called generalized mean or Hölder mean, and must not be
    confused with the Kolmogorov generalized mean, also called
    quasi-arithmetic mean or generalized f-mean [3]_.

    Parameters
    ----------
    a : array_like
        Input array, masked array or object that can be converted to an array.
    p : int or float
        Exponent. Must be finite.
    axis : int or None, optional
        Axis along which the power mean is computed. Default is 0.
        If None, compute over the whole array `a`.
    dtype : dtype, optional
        (Floating point) dtype to which numerical arguments are cast before performing
        the calculation. If `dtype` is not specified, it defaults to the floating point
        result dtype of the numerical arguments.
    weights : array_like, optional
        The weights array can either be 1-D (in which case its length must be
        the size of `a` along the given `axis`) or of the same shape as `a`.
        Default is None, which gives each value a weight of 1.0.

    Returns
    -------
    pmean : ndarray, see `dtype` parameter above.
        Output array containing the power mean values.

    See Also
    --------
    numpy.average : Weighted average
    gmean : Geometric mean
    hmean : Harmonic mean

    Notes
    -----
    The power mean is computed over a single dimension of the input
    array, ``axis=0`` by default, or all values in the array if ``axis=None``.
    float64 intermediate and return values are used for integer inputs.

    The power mean is only defined if all observations are non-negative;
    otherwise, the result is NaN.

    .. versionadded:: 1.9

    References
    ----------
    .. [1] "Generalized Mean", *Wikipedia*,
           https://en.wikipedia.org/wiki/Generalized_mean
    .. [2] Norris, N., "Convexity properties of generalized mean value
           functions", The Annals of Mathematical Statistics, vol. 8,
           pp. 118-120, 1937
    .. [3] Bullen, P.S., Handbook of Means and Their Inequalities, 2003

    Examples
    --------
    >>> from scipy.stats import pmean, hmean, gmean
    >>> pmean([1, 4], 1.3)
    2.639372938300652
    >>> pmean([1, 2, 3, 4, 5, 6, 7], 1.3)
    4.157111214492084
    >>> pmean([1, 4, 7], -2, weights=[3, 1, 3])
    1.4969684896631954

    For p=-1, power mean is equal to harmonic mean:

    >>> pmean([1, 4, 7], -1, weights=[3, 1, 3])
    1.9029126213592233
    >>> hmean([1, 4, 7], weights=[3, 1, 3])
    1.9029126213592233

    For p=0, power mean is defined as the geometric mean:

    >>> pmean([1, 4, 7], 0, weights=[3, 1, 3])
    2.80668351922014
    >>> gmean([1, 4, 7], weights=[3, 1, 3])
    2.80668351922014

    """
    if not isinstance(p, int | float):
        raise ValueError("Power mean only defined for exponent of type int or "
                         "float.")
    if p == 0:
        return gmean(a, axis=axis, dtype=dtype, weights=weights)
    elif math.isinf(p):
        message = "Power mean only implemented for finite `p`"
        raise NotImplementedError(message)

    xp = array_namespace(a, weights)
    dtype = (xp_result_type(a, p, weights, force_floating=True, xp=xp)
             if dtype is None else dtype)
    a = xp.asarray(a, dtype=dtype)

    if weights is not None:
        weights = xp.asarray(weights, dtype=dtype)

    negative_mask = a < 0
    a = xp.where(negative_mask, np.nan, a)

    if not is_lazy_array(negative_mask) and xp.any(negative_mask):
        message = ("The power mean is only defined if all elements are "
                   "non-negative; otherwise, the result is NaN.")
        warnings.warn(message, RuntimeWarning, stacklevel=2)

    # Linearized approximation for small p to avoid numerical issues; see gh-23407
    p_threshold = 2e-6
    if abs(p) <= p_threshold:
        return _linearized_pmean(a, p, axis=axis, weights=weights, xp=xp)

    with np.errstate(divide='ignore', invalid='ignore'):
        return _xp_mean(a**float(p), axis=axis, weights=weights)**(1/p)


def pmean(x, axis_name, *, axis_index_groups=None):
  """Compute an all-reduce mean on ``x`` over the pmapped axis ``axis_name``.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would perform pmeans over the first
      two and last two replicas). Groups must cover all axis indices exactly
      once, and on TPUs all groups must be the same size.

  Returns:
    Array(s) with the same shape as ``x`` representing the result of an
    all-reduce mean along the axis ``axis_name``.

  For example, with 4 XLA devices available:

  >>> x = np.arange(4)
  >>> y = jax.pmap(lambda x: jax.lax.pmean(x, 'i'), axis_name='i')(x)
  >>> print(y)
  [1.5 1.5 1.5 1.5]
  >>> y = jax.pmap(lambda x: x / jax.lax.pmean(x, 'i'), axis_name='i')(x)
  >>> print(y)
  [0.        0.6666667 1.3333334 2.       ]
  """
  x = psum(x, axis_name=axis_name, axis_index_groups=axis_index_groups)
  n = _axis_size(axis_name, axis_index_groups)
  return tree_util.tree_map(lambda v: v / n, x)

