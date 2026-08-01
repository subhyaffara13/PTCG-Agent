
def sem(a, axis=0, ddof=1):
    """
    Calculates the standard error of the mean of the input array.

    Also sometimes called standard error of measurement.

    Parameters
    ----------
    a : array_like
        An array containing the values for which the standard error is
        returned.
    axis : int or None, optional
        If axis is None, ravel `a` first. If axis is an integer, this will be
        the axis over which to operate. Defaults to 0.
    ddof : int, optional
        Delta degrees-of-freedom. How many degrees of freedom to adjust
        for bias in limited samples relative to the population estimate
        of variance. Defaults to 1.

    Returns
    -------
    s : ndarray or float
        The standard error of the mean in the sample(s), along the input axis.

    Notes
    -----
    The default value for `ddof` changed in scipy 0.15.0 to be consistent with
    `scipy.stats.sem` as well as with the most common definition used (like in
    the R documentation).

    Examples
    --------
    Find standard error along the first axis:

    >>> import numpy as np
    >>> from scipy import stats
    >>> a = np.arange(20).reshape(5,4)
    >>> print(stats.mstats.sem(a))
    [2.8284271247461903 2.8284271247461903 2.8284271247461903
     2.8284271247461903]

    Find standard error across the whole array, using n degrees of freedom:

    >>> print(stats.mstats.sem(a, axis=None, ddof=0))
    1.2893796958227628

    """
    a, axis = _chk_asarray(a, axis)
    n = a.count(axis=axis)
    s = a.std(axis=axis, ddof=ddof) / ma.sqrt(n)
    return s


def sem(a, axis=0, ddof=1, nan_policy='propagate'):
    """Compute standard error of the mean.

    Calculate the standard error of the mean (or standard error of
    measurement) of the values in the input array.

    Parameters
    ----------
    a : array_like
        An array containing the values for which the standard error is
        returned. Must contain at least two observations.
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    ddof : int, optional
        Delta degrees-of-freedom. How many degrees of freedom to adjust
        for bias in limited samples relative to the population estimate
        of variance. Defaults to 1.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': returns nan
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    Returns
    -------
    s : ndarray or float
        The standard error of the mean in the sample(s), along the input axis.

    Notes
    -----
    The default value for `ddof` is different to the default (0) used by other
    ddof containing routines, such as np.std and np.nanstd.

    Examples
    --------
    Find standard error along the first axis:

    >>> import numpy as np
    >>> from scipy import stats
    >>> a = np.arange(20).reshape(5,4)
    >>> stats.sem(a)
    array([ 2.8284,  2.8284,  2.8284,  2.8284])

    Find standard error across the whole array, using n degrees of freedom:

    >>> stats.sem(a, axis=None, ddof=0)
    1.2893796958227628

    """
    xp = array_namespace(a)
    if axis is None:
        a = xp.reshape(a, (-1,))
        axis = 0
    a = xpx.atleast_nd(xp.asarray(a), ndim=1, xp=xp)
    n = _count_nonmasked(a, axis, xp=xp)
    s = xp.std(a, axis=axis, correction=ddof) / n**0.5
    return s


def sem(a: ArrayLike, axis: int | None = 0, ddof: int = 1, nan_policy: str = "propagate", *, keepdims: bool = False) -> Array:
  """Compute the standard error of the mean.

  JAX implementation of :func:`scipy.stats.sem`.

  Args:
    a: arraylike
    axis: optional integer. If not specified, the input array is flattened.
    ddof: integer, default=1. The degrees of freedom in the SEM computation.
    nan_policy: str, default="propagate". JAX supports only "propagate" and
      "omit".
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.

  Returns:
    array

  Examples:
    >>> x = jnp.array([2, 4, 1, 1, 3, 4, 4, 2, 3])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x)
    Array(0.41, dtype=float32)

    For multi dimensional arrays, ``sem`` computes standard error of mean along
    ``axis=0``:

    >>> x1 = jnp.array([[1, 2, 1, 3, 2, 1],
    ...                 [3, 1, 3, 2, 1, 3],
    ...                 [1, 2, 2, 3, 1, 2]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x1)
    Array([0.67, 0.33, 0.58, 0.33, 0.33, 0.58], dtype=float32)

    If ``axis=1``, standard error of mean will be computed along ``axis 1``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x1, axis=1)
    Array([0.33, 0.4 , 0.31], dtype=float32)

    If ``axis=None``, standard error of mean will be computed along all the axes.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x1, axis=None)
    Array(0.2, dtype=float32)

    By default, ``sem`` reduces the dimension of the result. To keep the
    dimensions same as that of the input array, the argument ``keepdims`` must
    be set to ``True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x1, axis=1, keepdims=True)
    Array([[0.33],
           [0.4 ],
           [0.31]], dtype=float32)

    Since, by default, ``nan_policy='propagate'``, ``sem`` propagates the ``nan``
    values in the result.

    >>> nan = np.nan
    >>> x2 = jnp.array([[1, 2, 3, nan, 4, 2],
    ...                 [4, 5, 4, 3, nan, 1],
    ...                 [7, nan, 8, 7, 9, nan]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x2)
    Array([1.73,  nan, 1.53,  nan,  nan,  nan], dtype=float32)

    If ``nan_policy='omit```, ``sem`` omits the ``nan`` values and computes the error
    for the remaining values along the specified axis.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jax.scipy.stats.sem(x2, nan_policy='omit')
    Array([1.73, 1.5 , 1.53, 2.  , 2.5 , 0.5 ], dtype=float32)
  """
  b, = promote_args_inexact("sem", a)
  if nan_policy == "propagate":
    size = b.size if axis is None else b.shape[axis]
    return b.std(axis, ddof=ddof, keepdims=keepdims) / jnp.sqrt(size).astype(b.dtype)
  elif nan_policy == "omit":
    count = (~jnp.isnan(b)).sum(axis, keepdims=keepdims)
    return jnp.nanstd(b, axis, ddof=ddof, keepdims=keepdims) / jnp.sqrt(count).astype(b.dtype)
  else:
    raise ValueError(f"{nan_policy} is not supported")

