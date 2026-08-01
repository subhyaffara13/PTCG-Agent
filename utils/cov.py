
def cov(
    m: ArrayLike,
    y: ArrayLike | None = None,
    rowvar=True,
    bias=False,
    ddof=None,
    fweights: ArrayLike | None = None,
    aweights: ArrayLike | None = None,
    *,
    dtype: DTypeLike | None = None,
):
    m = _xy_helper_corrcoef(m, y, rowvar)

    if ddof is None:
        ddof = 1 if bias == 0 else 0

    is_half = (m.dtype == torch.float16) and m.is_cpu
    if is_half:
        # work around torch's "addmm_impl_cpu_" not implemented for 'Half'"
        dtype = torch.float32

    m = _util.cast_if_needed(m, dtype)
    result = torch.cov(m, correction=ddof, aweights=aweights, fweights=fweights)

    if is_half:
        result = result.to(torch.float16)

    return result


def cov(m: Array, /, *, xp: ModuleType | None = None) -> Array:
    """
    Estimate a covariance matrix (or a stack of covariance matrices).

    Covariance indicates the level to which two variables vary together.
    If we examine *N*-dimensional samples, :math:`X = [x_1, x_2, ... x_N]^T`,
    each with *M* observations, then element :math:`C_{ij}` of the
    :math:`N \times N` covariance matrix is the covariance of
    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance
    of :math:`x_i`.

    With the exception of supporting batch input, this provides a subset of
    the functionality of ``numpy.cov``.

    Parameters
    ----------
    m : array
        An array of shape ``(..., N, M)`` whose innermost two dimensions
        contain *M* observations of *N* variables. That is,
        each row of `m` represents a variable, and each column a single
        observation of all those variables.
    xp : array_namespace, optional
        The standard-compatible namespace for `m`. Default: infer.

    Returns
    -------
    array
        An array having shape (..., N, N) whose innermost two dimensions represent
        the covariance matrix of the variables.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx

    Consider two variables, :math:`x_0` and :math:`x_1`, which
    correlate perfectly, but in opposite directions:

    >>> x = xp.asarray([[0, 2], [1, 1], [2, 0]]).T
    >>> x
    Array([[0, 1, 2],
           [2, 1, 0]], dtype=array_api_strict.int64)

    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance
    matrix shows this clearly:

    >>> xpx.cov(x, xp=xp)
    Array([[ 1., -1.],
           [-1.,  1.]], dtype=array_api_strict.float64)

    Note that element :math:`C_{0,1}`, which shows the correlation between
    :math:`x_0` and :math:`x_1`, is negative.

    Further, note how `x` and `y` are combined:

    >>> x = xp.asarray([-2.1, -1,  4.3])
    >>> y = xp.asarray([3,  1.1,  0.12])
    >>> X = xp.stack((x, y), axis=0)
    >>> xpx.cov(X, xp=xp)
    Array([[11.71      , -4.286     ],
           [-4.286     ,  2.14413333]], dtype=array_api_strict.float64)

    >>> xpx.cov(x, xp=xp)
    Array(11.71, dtype=array_api_strict.float64)

    >>> xpx.cov(y, xp=xp)
    Array(2.14413333, dtype=array_api_strict.float64)

    Input with more than two dimensions is treated as a stack of
    two-dimensional input.

    >>> stack = xp.stack((X, 2*X))
    >>> xpx.cov(stack)
    Array([[[ 11.71      ,  -4.286     ],
            [ -4.286     ,   2.14413333]],

           [[ 46.84      , -17.144     ],
            [-17.144     ,   8.57653333]]], dtype=array_api_strict.float64)
    """

    if xp is None:
        xp = array_namespace(m)

    if (
        is_numpy_namespace(xp)
        or is_cupy_namespace(xp)
        or is_torch_namespace(xp)
        or is_dask_namespace(xp)
        or is_jax_namespace(xp)
    ) and m.ndim <= 2:
        return xp.cov(m)

    return _funcs.cov(m, xp=xp)


def cov(m: Array, /, *, xp: ModuleType) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in array_api_extra._delegation."""
    m = xp.asarray(m, copy=True)
    dtype = (
        xp.float64 if xp.isdtype(m.dtype, "integral") else xp.result_type(m, xp.float64)
    )

    m = atleast_nd(m, ndim=2, xp=xp)
    m = xp.astype(m, dtype)

    avg = _helpers.mean(m, axis=-1, keepdims=True, xp=xp)

    m_shape = eager_shape(m)
    fact = m_shape[-1] - 1

    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice", RuntimeWarning, stacklevel=2)
        fact = 0

    m -= avg
    m_transpose = xp.matrix_transpose(m)
    if xp.isdtype(m_transpose.dtype, "complex floating"):
        m_transpose = xp.conj(m_transpose)
    c = xp.matmul(m, m_transpose)
    c /= fact
    axes = tuple(axis for axis, length in enumerate(c.shape) if length == 1)
    return xp.squeeze(c, axis=axes)


def cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None,
        aweights=None, *, dtype=None):
    """
    Estimate a covariance matrix, given data and weights.

    Covariance indicates the level to which two variables vary together.
    If we examine N-dimensional samples, :math:`X = [x_1, x_2, ..., x_N]^T`,
    then the covariance matrix element :math:`C_{ij}` is the covariance of
    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance
    of :math:`x_i`.

    See the notes for an outline of the algorithm.

    Parameters
    ----------
    m : array_like
        A 1-D or 2-D array containing multiple variables and observations.
        Each row of `m` represents a variable, and each column a single
        observation of all those variables. Also see `rowvar` below.
    y : array_like, optional
        An additional set of variables and observations. `y` has the same form
        as that of `m`.
    rowvar : bool, optional
        If `rowvar` is True (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
    bias : bool, optional
        Default normalization (False) is by ``(N - 1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``. These values can be overridden by using
        the keyword ``ddof`` in numpy versions >= 1.5.
    ddof : int, optional
        If not ``None`` the default value implied by `bias` is overridden.
        Note that ``ddof=1`` will return the unbiased estimate, even if both
        `fweights` and `aweights` are specified, and ``ddof=0`` will return
        the simple average. See the notes for the details. The default value
        is ``None``.
    fweights : array_like, int, optional
        1-D array of integer frequency weights; the number of times each
        observation vector should be repeated.
    aweights : array_like, optional
        1-D array of observation vector weights. These relative weights are
        typically large for observations considered "important" and smaller for
        observations considered less "important". If ``ddof=0`` the array of
        weights can be used to assign probabilities to observation vectors.
    dtype : data-type, optional
        Data-type of the result. By default, the return data-type will have
        at least `numpy.float64` precision.

        .. versionadded:: 1.20

    Returns
    -------
    out : ndarray
        The covariance matrix of the variables.

    See Also
    --------
    corrcoef : Normalized covariance matrix

    Notes
    -----
    Assume that the observations are in the columns of the observation
    array `m` and let ``f = fweights`` and ``a = aweights`` for brevity. The
    steps to compute the weighted covariance are as follows::

        >>> m = np.arange(10, dtype=np.float64)
        >>> f = np.arange(10) * 2
        >>> a = np.arange(10) ** 2.
        >>> ddof = 1
        >>> w = f * a
        >>> v1 = np.sum(w)
        >>> v2 = np.sum(w * a)
        >>> m -= np.sum(m * w, axis=None, keepdims=True) / v1
        >>> cov = np.dot(m * w, m.T) * v1 / (v1**2 - ddof * v2)

    Note that when ``a == 1``, the normalization factor
    ``v1 / (v1**2 - ddof * v2)`` goes over to ``1 / (np.sum(f) - ddof)``
    as it should.

    Examples
    --------
    >>> import numpy as np

    Consider two variables, :math:`x_0` and :math:`x_1`, which
    correlate perfectly, but in opposite directions:

    >>> x = np.array([[0, 2], [1, 1], [2, 0]]).T
    >>> x
    array([[0, 1, 2],
           [2, 1, 0]])

    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance
    matrix shows this clearly:

    >>> np.cov(x)
    array([[ 1., -1.],
           [-1.,  1.]])

    Note that element :math:`C_{0,1}`, which shows the correlation between
    :math:`x_0` and :math:`x_1`, is negative.

    Further, note how `x` and `y` are combined:

    >>> x = [-2.1, -1,  4.3]
    >>> y = [3,  1.1,  0.12]
    >>> X = np.stack((x, y), axis=0)
    >>> np.cov(X)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x, y)
    array([[11.71      , -4.286     ], # may vary
           [-4.286     ,  2.144133]])
    >>> np.cov(x)
    array(11.71)

    """
    # Check inputs
    if ddof is not None and ddof != int(ddof):
        raise ValueError(
            "ddof must be integer")

    # Handles complex arrays too
    m = np.asarray(m)
    if m.ndim > 2:
        raise ValueError("m has more than 2 dimensions")

    if y is not None:
        y = np.asarray(y)
        if y.ndim > 2:
            raise ValueError("y has more than 2 dimensions")

    if dtype is None:
        if y is None:
            dtype = np.result_type(m, np.float64)
        else:
            dtype = np.result_type(m, y, np.float64)

    X = array(m, ndmin=2, dtype=dtype)
    if not rowvar and m.ndim != 1:
        X = X.T
    if X.shape[0] == 0:
        return np.array([]).reshape(0, 0)
    if y is not None:
        y = array(y, copy=None, ndmin=2, dtype=dtype)
        if not rowvar and y.shape[0] != 1:
            y = y.T
        X = np.concatenate((X, y), axis=0)

    if ddof is None:
        if bias == 0:
            ddof = 1
        else:
            ddof = 0

    # Get the product of frequencies and weights
    w = None
    if fweights is not None:
        fweights = np.asarray(fweights, dtype=float)
        if not np.all(fweights == np.around(fweights)):
            raise TypeError(
                "fweights must be integer")
        if fweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional fweights")
        if fweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and fweights")
        if any(fweights < 0):
            raise ValueError(
                "fweights cannot be negative")
        w = fweights
    if aweights is not None:
        aweights = np.asarray(aweights, dtype=float)
        if aweights.ndim > 1:
            raise RuntimeError(
                "cannot handle multidimensional aweights")
        if aweights.shape[0] != X.shape[1]:
            raise RuntimeError(
                "incompatible numbers of samples and aweights")
        if any(aweights < 0):
            raise ValueError(
                "aweights cannot be negative")
        if w is None:
            w = aweights
        else:
            w *= aweights

    avg, w_sum = average(X, axis=1, weights=w, returned=True)
    w_sum = w_sum[0]

    # Determine the normalization
    if w is None:
        fact = X.shape[1] - ddof
    elif ddof == 0:
        fact = w_sum
    elif aweights is None:
        fact = w_sum - ddof
    else:
        fact = w_sum - ddof * sum(w * aweights) / w_sum

    if fact <= 0:
        warnings.warn("Degrees of freedom <= 0 for slice",
                      RuntimeWarning, stacklevel=2)
        fact = 0.0

    X -= avg[:, None]
    if w is None:
        X_T = X.T
    else:
        X_T = (X * w).T
    c = dot(X, X_T.conj())
    c *= np.true_divide(1, fact)
    return c.squeeze()


def cov(x, y=None, rowvar=True, bias=False, allow_masked=True, ddof=None):
    """
    Estimate the covariance matrix.

    Except for the handling of missing data this function does the same as
    `numpy.cov`. For more details and examples, see `numpy.cov`.

    By default, masked values are recognized as such. If `x` and `y` have the
    same shape, a common mask is allocated: if ``x[i,j]`` is masked, then
    ``y[i,j]`` will also be masked.
    Setting `allow_masked` to False will raise an exception if values are
    missing in either of the input arrays.

    Parameters
    ----------
    x : array_like
        A 1-D or 2-D array containing multiple variables and observations.
        Each row of `x` represents a variable, and each column a single
        observation of all those variables. Also see `rowvar` below.
    y : array_like, optional
        An additional set of variables and observations. `y` has the same
        shape as `x`.
    rowvar : bool, optional
        If `rowvar` is True (default), then each row represents a
        variable, with observations in the columns. Otherwise, the relationship
        is transposed: each column represents a variable, while the rows
        contain observations.
    bias : bool, optional
        Default normalization (False) is by ``(N-1)``, where ``N`` is the
        number of observations given (unbiased estimate). If `bias` is True,
        then normalization is by ``N``. This keyword can be overridden by
        the keyword ``ddof`` in numpy versions >= 1.5.
    allow_masked : bool, optional
        If True, masked values are propagated pair-wise: if a value is masked
        in `x`, the corresponding value is masked in `y`.
        If False, raises a `ValueError` exception when some values are missing.
    ddof : {None, int}, optional
        If not ``None`` normalization is by ``(N - ddof)``, where ``N`` is
        the number of observations; this overrides the value implied by
        ``bias``. The default value is ``None``.

    Raises
    ------
    ValueError
        Raised if some values are missing and `allow_masked` is False.

    See Also
    --------
    numpy.cov

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([[0, 1], [1, 1]], mask=[0, 1, 0, 1])
    >>> y = np.ma.array([[1, 0], [0, 1]], mask=[0, 0, 1, 1])
    >>> np.ma.cov(x, y)
    masked_array(
    data=[[--, --, --, --],
          [--, --, --, --],
          [--, --, --, --],
          [--, --, --, --]],
    mask=[[ True,  True,  True,  True],
          [ True,  True,  True,  True],
          [ True,  True,  True,  True],
          [ True,  True,  True,  True]],
    fill_value=1e+20,
    dtype=float64)

    """
    # Check inputs
    if ddof is not None and ddof != int(ddof):
        raise ValueError("ddof must be an integer")
    # Set up ddof
    if ddof is None:
        if bias:
            ddof = 0
        else:
            ddof = 1

    (x, xnotmask, rowvar) = _covhelper(x, y, rowvar, allow_masked)
    if not rowvar:
        fact = np.dot(xnotmask.T, xnotmask) - ddof
        mask = np.less_equal(fact, 0, dtype=bool)
        with np.errstate(divide="ignore", invalid="ignore"):
            data = np.dot(filled(x.T, 0), filled(x.conj(), 0)) / fact
        result = ma.array(data, mask=mask).squeeze()
    else:
        fact = np.dot(xnotmask, xnotmask.T) - ddof
        mask = np.less_equal(fact, 0, dtype=bool)
        with np.errstate(divide="ignore", invalid="ignore"):
            data = np.dot(filled(x, 0), filled(x.T.conj(), 0)) / fact
        result = ma.array(data, mask=mask).squeeze()
    return result


def cov(m: ArrayLike, y: ArrayLike | None = None, rowvar: bool = True,
        bias: bool = False, ddof: int | None = None,
        fweights: ArrayLike | None = None,
        aweights: ArrayLike | None = None,
        dtype: DTypeLike | None = None) -> Array:
  r"""Estimate the weighted sample covariance.

  JAX implementation of :func:`numpy.cov`.

  The covariance :math:`C_{ij}` between variable *i* and variable *j* is defined
  as

  .. math::

     cov[X_i, X_j] = E[(X_i - E[X_i])(X_j - E[X_j])]

  Given an array of *N* observations of the variables :math:`X_i` and :math:`X_j`,
  this can be estimated via the sample covariance:

  .. math::

     C_{ij} = \frac{1}{N - 1} \sum_{n=1}^N (X_{in} - \overline{X_i})(X_{jn} - \overline{X_j})

  Where :math:`\overline{X_i} = \frac{1}{N} \sum_{k=1}^N X_{ik}` is the mean of the
  observations.

  Args:
    m: array of shape ``(M, N)`` (if ``rowvar`` is True), or ``(N, M)``
      (if ``rowvar`` is False) representing ``N`` observations of ``M`` variables.
      ``m`` may also be one-dimensional, representing ``N`` observations of a
      single variable.
    y: optional set of additional observations, with the same form as ``m``. If
      specified, then ``y`` is combined with ``m``, i.e. for the default
      ``rowvar = True`` case, ``m`` becomes ``jnp.vstack([m, y])``.
    rowvar: if True (default) then each row of ``m`` represents a variable. If
      False, then each column represents a variable.
    bias: if False (default) then normalize the covariance by ``N - 1``. If True,
      then normalize the covariance by ``N``
    ddof: specify the degrees of freedom. Defaults to ``1`` if ``bias`` is False,
      or to ``0`` if ``bias`` is True.
    fweights: optional array of integer frequency weights of shape ``(N,)``. This
      is an absolute weight specifying the number of times each observation is
      included in the computation.
    aweights: optional array of observation weights of shape ``(N,)``. This is
      a relative weight specifying the "importance" of each observation. In the
      ``ddof=0`` case, it is equivalent to assigning probabilities to each
      observation.
    dtype: optional data type of the result. Must be a float or complex type;
      if not specified, it will be determined based on the dtype of the input.

  Returns:
    A covariance matrix of shape ``(M, M)``, or a scalar with shape ``()`` if ``M = 1``.

  See also:
    - :func:`jax.numpy.corrcoef`: compute the correlation coefficient, a normalized
      version of the covariance matrix.

  Examples:
    Consider these observations of two variables that correlate perfectly.
    The covariance matrix in this case is a 2x2 matrix of ones:

    >>> x = jnp.array([[0, 1, 2],
    ...                [0, 1, 2]])
    >>> jnp.cov(x)
    Array([[1., 1.],
           [1., 1.]], dtype=float32)

    Now consider these observations of two variables that are perfectly
    anti-correlated. The covariance matrix in this case has ``-1`` in the
    off-diagonal:

    >>> x = jnp.array([[-1,  0,  1],
    ...                [ 1,  0, -1]])
    >>> jnp.cov(x)
    Array([[ 1., -1.],
           [-1.,  1.]], dtype=float32)

    Equivalently, these sequences can be specified as separate arguments,
    in which case they are stacked before continuing the computation.

    >>> x = jnp.array([-1, 0, 1])
    >>> y = jnp.array([1, 0, -1])
    >>> jnp.cov(x, y)
    Array([[ 1., -1.],
           [-1.,  1.]], dtype=float32)

    In general, the entries of the covariance matrix may be any positive
    or negative real value. For example, here is the covariance of 100
    points drawn from a 3-dimensional standard normal distribution:

    >>> key = jax.random.key(0)
    >>> x = jax.random.normal(key, shape=(3, 100))
    >>> with jnp.printoptions(precision=2):
    ...   print(jnp.cov(x))
    [[0.9  0.03 0.1 ]
     [0.03 1.   0.01]
     [0.1  0.01 0.85]]
  """
  if y is not None:
    m, y = util.promote_args_inexact("cov", m, y)
    if y.ndim > 2:
      raise ValueError("y has more than 2 dimensions")
  else:
    m, = util.promote_args_inexact("cov", m)

  if m.ndim > 2:
    raise ValueError("m has more than 2 dimensions")  # same as numpy error

  if dtype is not None and not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"cov: dtype must be a subclass of float or complex; got {dtype=}")

  X = atleast_2d(m)
  if not rowvar and m.ndim != 1:
    X = X.T
  if X.shape[0] == 0:
    return array([]).reshape(0, 0)

  if y is not None:
    y_arr = atleast_2d(y)
    if not rowvar and y_arr.shape[0] != 1:
      y_arr = y_arr.T
    X = concatenate((X, y_arr), axis=0)
  if X.shape[1] == 0:
    cov_shape = () if X.shape[0] == 1 else (X.shape[0], X.shape[0])
    return array_creation.full(cov_shape, np.nan, dtype=X.dtype)

  if ddof is None:
    ddof = 1 if bias == 0 else 0

  w: Array | None = None
  if fweights is not None:
    fweights = util.ensure_arraylike("cov", fweights)
    if np.ndim(fweights) > 1:
      raise RuntimeError("cannot handle multidimensional fweights")
    if np.shape(fweights)[0] != X.shape[1]:
      raise RuntimeError("incompatible numbers of samples and fweights")
    if not issubdtype(fweights.dtype, np.integer):
      raise TypeError("fweights must be integer.")
    # Ensure positive fweights; note that numpy raises an error on negative fweights.
    w = abs(fweights)
  if aweights is not None:
    aweights = util.ensure_arraylike("cov", aweights)
    if np.ndim(aweights) > 1:
      raise RuntimeError("cannot handle multidimensional aweights")
    if np.shape(aweights)[0] != X.shape[1]:
      raise RuntimeError("incompatible numbers of samples and aweights")
    # Ensure positive aweights: note that numpy raises an error for negative aweights.
    aweights = abs(aweights)
    w = asarray(aweights if w is None else w * aweights)

  if dtype is not None:
    X = X.astype(dtype)
    w = w.astype(dtype) if w is not None else w

  avg, w_sum = reductions.average(X, axis=1, weights=w, returned=True)
  w_sum = w_sum[0]

  if w is None:
    f = X.shape[1] - ddof
  elif ddof == 0:
    f = w_sum
  elif aweights is None:
    f = w_sum - ddof
  else:
    f = w_sum - ddof * reductions.sum(w * aweights) / w_sum

  X = X - avg[:, None]
  X_T = X.T if w is None else (X * lax.broadcast_to_rank(w, X.ndim)).T
  return ufuncs.true_divide(tensor_contractions.dot(X, X_T.conj()), f).squeeze()

