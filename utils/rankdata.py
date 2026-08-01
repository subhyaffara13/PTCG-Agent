
def rankdata(data, axis=None, use_missing=False):
    """Returns the rank (also known as order statistics) of each data point
    along the given axis.

    If some values are tied, their rank is averaged.
    If some values are masked, their rank is set to 0 if use_missing is False,
    or set to the average rank of the unmasked values if use_missing is True.

    Parameters
    ----------
    data : sequence
        Input data. The data is transformed to a masked array
    axis : {None,int}, optional
        Axis along which to perform the ranking.
        If None, the array is first flattened. An exception is raised if
        the axis is specified for arrays with a dimension larger than 2
    use_missing : bool, optional
        Whether the masked values have a rank of 0 (False) or equal to the
        average rank of the unmasked values (True).

    """  # numpydoc ignore=RT01
    def _rank1d(data, use_missing=False):
        n = data.count()
        rk = np.empty(data.size, dtype=float)
        idx = data.argsort()
        rk[idx[:n]] = np.arange(1,n+1)

        if use_missing:
            rk[idx[n:]] = (n+1)/2.
        else:
            rk[idx[n:]] = 0

        repeats = find_repeats(data.copy())
        for r in repeats[0]:
            condition = (data == r).filled(False)
            rk[condition] = rk[condition].mean()
        return rk

    data = ma.array(data, copy=False)
    if axis is None:
        if data.ndim > 1:
            return _rank1d(data.ravel(), use_missing).reshape(data.shape)
        else:
            return _rank1d(data, use_missing)
    else:
        return ma.apply_along_axis(_rank1d,axis,data,use_missing).view(ndarray)


def rankdata(a, method='average', *, axis=None, nan_policy='propagate'):
    """Assign ranks to data, dealing with ties appropriately.

    By default (``axis=None``), the data array is first flattened, and a flat
    array of ranks is returned. Separately reshape the rank array to the
    shape of the data array if desired (see Examples).

    Ranks begin at 1.  The `method` argument controls how ranks are assigned
    to equal values.  See [1]_ for further discussion of ranking methods.

    Parameters
    ----------
    a : array_like
        The array of values to be ranked.
    method : {'average', 'min', 'max', 'dense', 'ordinal'}, optional
        The method used to assign ranks to tied elements.
        The following methods are available (default is 'average'):

        * 'average': The average of the ranks that would have been assigned to
          all the tied values is assigned to each value.
        * 'min': The minimum of the ranks that would have been assigned to all
          the tied values is assigned to each value.  (This is also
          referred to as "competition" ranking.)
        * 'max': The maximum of the ranks that would have been assigned to all
          the tied values is assigned to each value.
        * 'dense': Like 'min', but the rank of the next highest element is
          assigned the rank immediately after those assigned to the tied
          elements.
        * 'ordinal': All values are given a distinct rank, corresponding to
          the order that the values occur in `a`.

    axis : {None, int}, optional
        Axis along which to perform the ranking. If ``None``, the data array
        is first flattened.
    nan_policy : {'propagate', 'omit', 'raise'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': propagates nans through the rank calculation
        * 'omit': performs the calculations ignoring nan values
        * 'raise': raises an error

        .. note::

            When `nan_policy` is 'propagate', the output is an array of *all*
            nans because ranks relative to nans in the input are undefined.
            When `nan_policy` is 'omit', nans in `a` are ignored when ranking
            the other values, and the corresponding locations of the output
            are nan.

        .. versionadded:: 1.10

    Returns
    -------
    ranks : ndarray
         An array of size equal to the size of `a`, containing rank
         scores. The dtype is the result dtype of `a` and a Python float.

    References
    ----------
    .. [1] "Ranking", https://en.wikipedia.org/wiki/Ranking

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats import rankdata
    >>> rankdata([0, 2, 3, 2])
    array([1. , 2.5, 4. , 2.5])
    >>> rankdata([0, 2, 3, 2], method='min')
    array([1., 2., 4., 2.])
    >>> rankdata([0, 2, 3, 2], method='max')
    array([1., 3., 4., 3.])
    >>> rankdata([0, 2, 3, 2], method='dense')
    array([1., 2., 3., 2.])
    >>> rankdata([0, 2, 3, 2], method='ordinal')
    array([1., 2., 4., 3.])
    >>> rankdata([[0, 2], [3, 2]]).reshape(2, 2)
    array([[1. , 2.5],
           [4. , 2.5]])
    >>> rankdata([[0, 2, 2], [3, 2, 5]], axis=1)
    array([[1. , 2.5, 2.5],
           [2. , 1. , 3. ]])
    >>> rankdata([0, 2, 3, np.nan, -2, np.nan], nan_policy="propagate")
    array([nan, nan, nan, nan, nan, nan])
    >>> rankdata([0, 2, 3, np.nan, -2, np.nan], nan_policy="omit")
    array([ 2.,  3.,  4., nan,  1., nan])

    """
    methods = ('average', 'min', 'max', 'dense', 'ordinal')
    if method not in methods:
        raise ValueError(f'unknown method "{method}"')

    xp = array_namespace(a)
    x = xp.asarray(a)

    if axis is None:
        x = xp_ravel(x)
        axis = -1

    if xp_size(x) == 0:
        dtype = xp_result_type(x, force_floating=True, xp=xp)
        return xp.empty_like(x, dtype=dtype)

    contains_nan = _contains_nan(x, nan_policy)

    x = xp_swapaxes(x, axis, -1, xp=xp)
    ranks, _, _ = _rankdata(x, method, xp=xp)

    # JIT won't allow use of `contains_nan` for control flow here, so we always have to
    # run this with JIT.
    if is_lazy_array(x) or contains_nan:
        i_nan = (xp.isnan(x) if nan_policy == 'omit'
                 else xp.any(xp.isnan(x), axis=-1, keepdims=True))
        i_nan = xp.broadcast_to(i_nan, ranks.shape)
        ranks = xpx.at(ranks)[i_nan].set(xp.nan)

    ranks = xp_swapaxes(ranks, axis, -1, xp=xp)
    return ranks


def rankdata(
  a: ArrayLike,
  method: str = "average",
  *,
  axis: int | None = None,
  nan_policy: str = "propagate",
) -> Array:
  """Compute the rank of data along an array axis.

  JAX implementation of :func:`scipy.stats.rankdata`.

  Ranks begin at 1, and the *method* argument controls how ties are handled.

  Args:
    a: arraylike
    method: str, default="average". Supported methods are
      ``("average", "min", "max", "dense", "ordinal")``
      For details, see the :func:`scipy.stats.rankdata` documentation.
    axis: optional integer. If not specified, the input array is flattened.
    nan_policy: str, JAX's implementation only supports ``"propagate"``.

  Returns:
    array of ranks along the specified axis.

  Examples:

    >>> x = jnp.array([10, 30, 20])
    >>> rankdata(x)
    Array([1., 3., 2.], dtype=float32)

    >>> x = jnp.array([1, 3, 2, 3])
    >>> rankdata(x)
    Array([1. , 3.5, 2. , 3.5], dtype=float32)
  """
  check_arraylike("rankdata", a)

  if nan_policy not in ["propagate", "omit", "raise"]:
    raise ValueError(
      f"Illegal nan_policy value {nan_policy!r}; expected one of "
      "{'propagate', 'omit', 'raise'}"
    )
  if nan_policy == "omit":
    raise NotImplementedError(
      f"Logic for `nan_policy` of {nan_policy} is not implemented"
    )
  if nan_policy == "raise":
    raise NotImplementedError(
      "In order to best JIT compile `rankdata`, we cannot know whether `x` "
      "contains nans. Please check if nans exist in `x` outside of the "
      "`rankdata` function."
    )

  if method not in ("average", "min", "max", "dense", "ordinal"):
    raise ValueError(f"unknown method '{method}'")

  if axis is not None:
    return jnp.apply_along_axis(rankdata, axis, a, method)

  a = jnp.ravel(a)
  out_dtype = dtypes.default_float_dtype()

  def _rankdata(a: Array) -> Array:
    arr, sorter = lax.sort_key_val(a, jnp.arange(a.size))
    inv = invert_permutation(sorter)

    if method == "ordinal":
      return (inv + 1).astype(out_dtype)
    obs = jnp.concatenate([jnp.array([True]), arr[1:] != arr[:-1]])
    dense = obs.cumsum()[inv]
    if method == "dense":
      return dense.astype(out_dtype)
    count = jnp.nonzero(obs, size=arr.size + 1, fill_value=obs.size)[0].astype(out_dtype)
    if method == "max":
      return count[dense]
    if method == "min":
      return count[dense - 1] + 1
    if method == "average":
      return .5 * (count[dense] + count[dense - 1] + 1)
    raise ValueError(f"unknown method '{method}'")

  return lax.cond(jnp.any(jnp.isnan(a)),
                  lambda a: jnp.full_like(a, jnp.nan, out_dtype),
                  _rankdata, a)

