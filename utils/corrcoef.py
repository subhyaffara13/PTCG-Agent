
def corrcoef(
    x: ArrayLike,
    y: ArrayLike | None = None,
    rowvar=True,
    bias=None,
    ddof=None,
    *,
    dtype: DTypeLike | None = None,
):
    if bias is not None or ddof is not None:
        # deprecated in NumPy
        raise NotImplementedError
    xy_tensor = _xy_helper_corrcoef(x, y, rowvar)

    is_half = (xy_tensor.dtype == torch.float16) and xy_tensor.is_cpu
    if is_half:
        # work around torch's "addmm_impl_cpu_" not implemented for 'Half'"
        dtype = torch.float32

    xy_tensor = _util.cast_if_needed(xy_tensor, dtype)
    result = torch.corrcoef(xy_tensor)

    if is_half:
        result = result.to(torch.float16)

    return result


def corrcoef(x, y=None, rowvar=True, *,
             dtype=None):
    """
    Return Pearson product-moment correlation coefficients.

    Please refer to the documentation for `cov` for more detail.  The
    relationship between the correlation coefficient matrix, `R`, and the
    covariance matrix, `C`, is

    .. math:: R_{ij} = \\frac{ C_{ij} } { \\sqrt{ C_{ii} C_{jj} } }

    The values of `R` are between -1 and 1, inclusive.

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

    dtype : data-type, optional
        Data-type of the result. By default, the return data-type will have
        at least `numpy.float64` precision.

        .. versionadded:: 1.20

    Returns
    -------
    R : ndarray
        The correlation coefficient matrix of the variables.

    See Also
    --------
    cov : Covariance matrix

    Notes
    -----
    Due to floating point rounding the resulting array may not be Hermitian,
    the diagonal elements may not be 1, and the elements may not satisfy the
    inequality abs(a) <= 1. The real and imaginary parts are clipped to the
    interval [-1,  1] in an attempt to improve on that situation but is not
    much help in the complex case.

    Examples
    --------
    >>> import numpy as np

    In this example we generate two random arrays, ``xarr`` and ``yarr``, and
    compute the row-wise and column-wise Pearson correlation coefficients,
    ``R``. Since ``rowvar`` is  true by  default, we first find the row-wise
    Pearson correlation coefficients between the variables of ``xarr``.

    >>> import numpy as np
    >>> rng = np.random.default_rng(seed=42)
    >>> xarr = rng.random((3, 3))
    >>> xarr
    array([[0.77395605, 0.43887844, 0.85859792],
           [0.69736803, 0.09417735, 0.97562235],
           [0.7611397 , 0.78606431, 0.12811363]])
    >>> R1 = np.corrcoef(xarr)
    >>> R1
    array([[ 1.        ,  0.99256089, -0.68080986],
           [ 0.99256089,  1.        , -0.76492172],
           [-0.68080986, -0.76492172,  1.        ]])

    If we add another set of variables and observations ``yarr``, we can
    compute the row-wise Pearson correlation coefficients between the
    variables in ``xarr`` and ``yarr``.

    >>> yarr = rng.random((3, 3))
    >>> yarr
    array([[0.45038594, 0.37079802, 0.92676499],
           [0.64386512, 0.82276161, 0.4434142 ],
           [0.22723872, 0.55458479, 0.06381726]])
    >>> R2 = np.corrcoef(xarr, yarr)
    >>> R2
    array([[ 1.        ,  0.99256089, -0.68080986,  0.75008178, -0.934284  ,
            -0.99004057],
           [ 0.99256089,  1.        , -0.76492172,  0.82502011, -0.97074098,
            -0.99981569],
           [-0.68080986, -0.76492172,  1.        , -0.99507202,  0.89721355,
             0.77714685],
           [ 0.75008178,  0.82502011, -0.99507202,  1.        , -0.93657855,
            -0.83571711],
           [-0.934284  , -0.97074098,  0.89721355, -0.93657855,  1.        ,
             0.97517215],
           [-0.99004057, -0.99981569,  0.77714685, -0.83571711,  0.97517215,
             1.        ]])

    Finally if we use the option ``rowvar=False``, the columns are now
    being treated as the variables and we will find the column-wise Pearson
    correlation coefficients between variables in ``xarr`` and ``yarr``.

    >>> R3 = np.corrcoef(xarr, yarr, rowvar=False)
    >>> R3
    array([[ 1.        ,  0.77598074, -0.47458546, -0.75078643, -0.9665554 ,
             0.22423734],
           [ 0.77598074,  1.        , -0.92346708, -0.99923895, -0.58826587,
            -0.44069024],
           [-0.47458546, -0.92346708,  1.        ,  0.93773029,  0.23297648,
             0.75137473],
           [-0.75078643, -0.99923895,  0.93773029,  1.        ,  0.55627469,
             0.47536961],
           [-0.9665554 , -0.58826587,  0.23297648,  0.55627469,  1.        ,
            -0.46666491],
           [ 0.22423734, -0.44069024,  0.75137473,  0.47536961, -0.46666491,
             1.        ]])

    """
    c = cov(x, y, rowvar, dtype=dtype)
    try:
        d = diag(c)
    except ValueError:
        # scalar covariance
        # nan if incorrect value (nan, inf, 0), 1 otherwise
        return c / c
    stddev = sqrt(d.real)
    c /= stddev[:, None]
    c /= stddev[None, :]

    # Clip real and imaginary parts to [-1, 1].  This does not guarantee
    # abs(a[i,j]) <= 1 for complex arrays, but is the best we can do without
    # excessive work.
    np.clip(c.real, -1, 1, out=c.real)
    if np.iscomplexobj(c):
        np.clip(c.imag, -1, 1, out=c.imag)

    return c


def corrcoef(x, y=None, rowvar=True, allow_masked=True,
             ):
    """
    Return Pearson product-moment correlation coefficients.

    Except for the handling of missing data this function does the same as
    `numpy.corrcoef`. For more details and examples, see `numpy.corrcoef`.

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
    allow_masked : bool, optional
        If True, masked values are propagated pair-wise: if a value is masked
        in `x`, the corresponding value is masked in `y`.
        If False, raises an exception.  Because `bias` is deprecated, this
        argument needs to be treated as keyword only to avoid a warning.

    See Also
    --------
    numpy.corrcoef : Equivalent function in top-level NumPy module.
    cov : Estimate the covariance matrix.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.ma.array([[0, 1], [1, 1]], mask=[0, 1, 0, 1])
    >>> np.ma.corrcoef(x)
    masked_array(
      data=[[--, --],
            [--, --]],
      mask=[[ True,  True],
            [ True,  True]],
      fill_value=1e+20,
      dtype=float64)

    """
    # Estimate the covariance matrix.
    corr = cov(x, y, rowvar, allow_masked=allow_masked)
    # The non-masked version returns a masked value for a scalar.
    try:
        std = ma.sqrt(ma.diagonal(corr))
    except ValueError:
        return ma.MaskedConstant()
    corr /= ma.multiply.outer(std, std)
    return corr


def corrcoef(x: ArrayLike, y: ArrayLike | None = None, rowvar: bool = True,
             dtype: DTypeLike | None = None) -> Array:
  r"""Compute the Pearson correlation coefficients.

  JAX implementation of :func:`numpy.corrcoef`.

  This is a normalized version of the sample covariance computed by :func:`jax.numpy.cov`.
  For a sample covariance :math:`C_{ij}`, the correlation coefficients are

  .. math::

     R_{ij} = \frac{C_{ij}}{\sqrt{C_{ii}C_{jj}}}

  they are constructed such that the values satisfy :math:`-1 \le R_{ij} \le 1`.

  Args:
    x: array of shape ``(M, N)`` (if ``rowvar`` is True), or ``(N, M)``
      (if ``rowvar`` is False) representing ``N`` observations of ``M`` variables.
      ``x`` may also be one-dimensional, representing ``N`` observations of a
      single variable.
    y: optional set of additional observations, with the same form as ``m``. If
      specified, then ``y`` is combined with ``m``, i.e. for the default
      ``rowvar = True`` case, ``m`` becomes ``jnp.vstack([m, y])``.
    rowvar: if True (default) then each row of ``m`` represents a variable. If
      False, then each column represents a variable.
    dtype: optional data type of the result. Must be a float or complex type;
      if not specified, it will be determined based on the dtype of the input.

  Returns:
    A covariance matrix of shape ``(M, M)``.

  See also:
    - :func:`jax.numpy.cov`: compute the covariance matrix.

  Examples:
    Consider these observations of two variables that correlate perfectly.
    The correlation matrix in this case is a 2x2 matrix of ones:

    >>> x = jnp.array([[0, 1, 2],
    ...                [0, 1, 2]])
    >>> jnp.corrcoef(x)
    Array([[1., 1.],
           [1., 1.]], dtype=float32)

    Now consider these observations of two variables that are perfectly
    anti-correlated. The correlation matrix in this case has ``-1`` in the
    off-diagonal:

    >>> x = jnp.array([[-1,  0,  1],
    ...                [ 1,  0, -1]])
    >>> jnp.corrcoef(x)
    Array([[ 1., -1.],
           [-1.,  1.]], dtype=float32)

    Equivalently, these sequences can be specified as separate arguments,
    in which case they are stacked before continuing the computation.

    >>> x = jnp.array([-1, 0, 1])
    >>> y = jnp.array([1, 0, -1])
    >>> jnp.corrcoef(x, y)
    Array([[ 1., -1.],
           [-1.,  1.]], dtype=float32)

    The entries of the correlation matrix are normalized such that they
    lie within the range -1 to +1, where +1 indicates perfect correlation
    and -1 indicates perfect anti-correlation. For example, here is the
    correlation of 100 points drawn from a 3-dimensional standard normal
    distribution:

    >>> key = jax.random.key(0)
    >>> x = jax.random.normal(key, shape=(3, 100))
    >>> with jnp.printoptions(precision=2):
    ...   print(jnp.corrcoef(x))
    [[1.   0.03 0.12]
     [0.03 1.   0.01]
     [0.12 0.01 1.  ]]
  """
  util.check_arraylike("corrcoef", x)
  if dtype is not None and not dtypes.issubdtype(dtype, np.inexact):
    raise ValueError(f"corrcoef: dtype must be a subclass of float or complex; got {dtype=}")
  c = cov(x, y, rowvar, dtype=dtype)
  if len(np.shape(c)) == 0:
    # scalar - this should yield nan for values (nan/nan, inf/inf, 0/0), 1 otherwise
    return ufuncs.divide(c, c)
  d = diag(c)
  stddev = ufuncs.sqrt(ufuncs.real(d)).astype(c.dtype)
  c = c / stddev[:, None] / stddev[None, :]

  real_part = clip(ufuncs.real(c), -1, 1)
  if iscomplexobj(c):
    complex_part = clip(ufuncs.imag(c), -1, 1)
    c = lax.complex(real_part, complex_part)
  else:
    c = real_part
  return c

