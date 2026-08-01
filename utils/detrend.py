
def detrend(x, key=None, axis=None):
    """
    Return *x* with its trend removed.

    Parameters
    ----------
    x : array or sequence
        Array or sequence containing the data.

    key : {'default', 'constant', 'mean', 'linear', 'none'} or function
        The detrending algorithm to use. 'default', 'mean', and 'constant' are
        the same as `detrend_mean`. 'linear' is the same as `detrend_linear`.
        'none' is the same as `detrend_none`. The default is 'mean'. See the
        corresponding functions for more details regarding the algorithms. Can
        also be a function that carries out the detrend operation.

    axis : int
        The axis along which to do the detrending.

    See Also
    --------
    detrend_mean : Implementation of the 'mean' algorithm.
    detrend_linear : Implementation of the 'linear' algorithm.
    detrend_none : Implementation of the 'none' algorithm.
    """
    if key is None or key in ['constant', 'mean', 'default']:
        return detrend(x, key=detrend_mean, axis=axis)
    elif key == 'linear':
        return detrend(x, key=detrend_linear, axis=axis)
    elif key == 'none':
        return detrend(x, key=detrend_none, axis=axis)
    elif callable(key):
        x = np.asarray(x)
        if axis is not None and axis + 1 > x.ndim:
            raise ValueError(f'axis(={axis}) out of bounds')
        if (axis is None and x.ndim == 0) or (not axis and x.ndim == 1):
            return key(x)
        # try to use the 'axis' argument if the function supports it,
        # otherwise use apply_along_axis to do it
        try:
            return key(x, axis=axis)
        except TypeError:
            return np.apply_along_axis(key, axis=axis, arr=x)
    else:
        raise ValueError(
            f"Unknown value for key: {key!r}, must be one of: 'default', "
            f"'constant', 'mean', 'linear', or a function")


def detrend(data: np.ndarray, axis: int = -1,
            type: Literal['linear', 'constant'] = 'linear',
            bp: ArrayLike | int = 0, overwrite_data: bool = False) -> np.ndarray:
    r"""Remove linear or constant trend along axis from data.

    Parameters
    ----------
    data : array_like
        The input data.
    axis : int, optional
        The axis along which to detrend the data. By default this is the
        last axis (-1).
    type : {'linear', 'constant'}, optional
        The type of detrending. If ``type == 'linear'`` (default),
        the result of a linear least-squares fit to `data` is subtracted
        from `data`.
        If ``type == 'constant'``, only the mean of `data` is subtracted.
    bp : array_like of ints, optional
        A sequence of break points. If given, an individual linear fit is
        performed for each part of `data` between two break points.
        Break points are specified as indices into `data`. This parameter
        only has an effect when ``type == 'linear'``.
    overwrite_data : bool, optional
        If True, allow in place detrending and avoid a copy. Default is
        False. In place modification applies only if ``type == 'linear'``
        and `data` is of the floating point dtype ``float32``, ``float64``,
        ``complex64`` or ``complex128``.

    Returns
    -------
    ret : ndarray
        The detrended input data.

    Notes
    -----
    Detrending can be interpreted as subtracting a least squares fit polynomial:
    Setting the parameter `type` to 'constant' corresponds to fitting a zeroth degree
    polynomial, 'linear' to a first degree polynomial. Consult the example below.

    See Also
    --------
    :meth:`numpy.polynomial.polynomial.Polynomial.fit` : Create least squares fit polynomial.


    Examples
    --------
    The following example detrends the function :math:`x(t) = \sin(\pi t) + 1/4`:

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> from scipy.signal import detrend
    ...
    >>> t = np.linspace(-0.5, 0.5, 21)
    >>> x = np.sin(np.pi*t) + 1/4
    ...
    >>> x_d_const = detrend(x, type='constant')
    >>> x_d_linear = detrend(x, type='linear')
    ...
    >>> fig1, ax1 = plt.subplots()
    >>> ax1.set_title(r"Detrending $x(t)=\sin(\pi t) + 1/4$")
    >>> ax1.set(xlabel="t", ylabel="$x(t)$", xlim=(t[0], t[-1]))
    >>> ax1.axhline(y=0, color='black', linewidth=.5)
    >>> ax1.axvline(x=0, color='black', linewidth=.5)
    >>> ax1.plot(t, x, 'C0.-',  label="No detrending")
    >>> ax1.plot(t, x_d_const, 'C1x-', label="type='constant'")
    >>> ax1.plot(t, x_d_linear, 'C2+-', label="type='linear'")
    >>> ax1.legend()
    >>> plt.show()

    Alternatively, NumPy's `~numpy.polynomial.polynomial.Polynomial` can be used for
    detrending as well:

    >>> pp0 = np.polynomial.Polynomial.fit(t, x, deg=0)  # fit degree 0 polynomial
    >>> np.allclose(x_d_const, x - pp0(t))  # compare with constant detrend
    True
    >>> pp1 = np.polynomial.Polynomial.fit(t, x, deg=1)  # fit degree 1 polynomial
    >>> np.allclose(x_d_linear, x - pp1(t))  # compare with linear detrend
    True

    Note that `~numpy.polynomial.polynomial.Polynomial` also allows fitting higher
    degree polynomials. Consult its documentation on how to extract the polynomial
    coefficients.
    """  # noqa: E501
    if type not in ['linear', 'l', 'constant', 'c']:
        raise ValueError("Trend type must be 'linear' or 'constant'.")

    xp = array_namespace(data, bp)

    data = np.asarray(data)
    dtype = data.dtype.char
    if dtype not in 'dfDF':
        dtype = 'd'
    if type in ['constant', 'c']:
        ret = data - np.mean(data, axis, keepdims=True)
        return xp.asarray(ret)
    else:
        dshape = data.shape
        N = dshape[axis]
        bp = np.asarray(bp)
        bp = np.sort(np.unique(np.concatenate(np.atleast_1d(0, bp, N))))
        if np.any(bp > N):
            raise ValueError("Breakpoints must be less than length "
                             "of data along given axis.")

        # Restructure data so that axis is along first dimension and
        #  all other dimensions are collapsed into second dimension
        rnk = len(dshape)
        if axis < 0:
            axis = axis + rnk
        newdata = np.moveaxis(data, axis, 0)
        newdata_shape = newdata.shape
        newdata = newdata.reshape(N, -1)

        if not overwrite_data:
            newdata = newdata.copy()  # make sure we have a copy
        if newdata.dtype.char not in 'dfDF':
            newdata = newdata.astype(dtype)

#        Nreg = len(bp) - 1
        # Find leastsq fit and remove it for each piece
        for m in range(len(bp) - 1):
            Npts = bp[m + 1] - bp[m]
            A = np.ones((Npts, 2), dtype)
            A[:, 0] = np.arange(1, Npts + 1, dtype=dtype) / Npts
            sl = slice(bp[m], bp[m + 1])
            coef, resids, rank, s = linalg.lstsq(A, newdata[sl])
            newdata[sl] = newdata[sl] - A @ coef

        # Put data back in original shape.
        newdata = newdata.reshape(newdata_shape)
        ret = np.moveaxis(newdata, 0, axis)
        return xp.asarray(ret)


def detrend(data: ArrayLike, axis: int = -1, type: str = 'linear',
            bp: int | Sequence[int] | np.ndarray = 0,
            overwrite_data: None = None) -> Array:
  """
  Remove linear or piecewise linear trends from data.

  JAX implementation of :func:`scipy.signal.detrend`.

  Args:
    data: The input array containing the data to detrend.
    axis: The axis along which to detrend. Default is -1 (the last axis).
    type: The type of detrending. Can be:

      * ``'linear'``: Fit a single linear trend for the entire data.
      * ``'constant'``: Remove the mean value of the data.

    bp: A sequence of breakpoints. If given, piecewise linear trends
      are fit between these breakpoints.
    overwrite_data: This argument is not supported by JAX's implementation.

  Returns:
    The detrended data array.

  Examples:
    A simple detrend operation in one dimension:

    >>> data = jnp.array([1., 4., 8., 8., 9.])

    Removing a linear trend from the data:

    >>> detrended = jax.scipy.signal.detrend(data)
    >>> with jnp.printoptions(precision=3, suppress=True):  # suppress float error
    ...   print("Detrended:", detrended)
    ...   print("Underlying trend:", data - detrended)
    Detrended: [-1. -0.  2. -0. -1.]
    Underlying trend: [ 2.  4.  6.  8. 10.]

    Removing a constant trend from the data:

    >>> detrended = jax.scipy.signal.detrend(data, type='constant')
    >>> with jnp.printoptions(precision=3):  # suppress float error
    ...   print("Detrended:", detrended)
    ...   print("Underlying trend:", data - detrended)
    Detrended: [-5. -2.  2.  2.  3.]
    Underlying trend: [6. 6. 6. 6. 6.]
  """
  if overwrite_data is not None:
    raise NotImplementedError("overwrite_data argument not implemented.")
  if type not in ['constant', 'linear']:
    raise ValueError("Trend type must be 'linear' or 'constant'.")
  data_arr, = promote_dtypes_inexact(jnp.asarray(data))
  if type == 'constant':
    return data_arr - data_arr.mean(axis, keepdims=True)
  else:
    N = data_arr.shape[axis]
    # bp is static, so we use np operations to avoid pushing to device.
    bp_arr = np.sort(np.unique(np.r_[0, bp, N]))
    if bp_arr[0] < 0 or bp_arr[-1] > N:
      raise ValueError("Breakpoints must be non-negative and less than length of data along given axis.")
    data_arr = jnp.moveaxis(data_arr, axis, 0)
    shape = data_arr.shape
    data_arr = data_arr.reshape(N, -1)
    for m in range(len(bp_arr) - 1):
      Npts = bp_arr[m + 1] - bp_arr[m]
      A = jnp.vstack([
        jnp.ones(Npts, dtype=data_arr.dtype),
        jnp.arange(1, Npts + 1, dtype=data_arr.dtype) / Npts.astype(data_arr.dtype)
      ]).T
      sl = slice(bp_arr[m], bp_arr[m + 1])
      coef, *_ = linalg.lstsq(A, data_arr[sl])
      data_arr = data_arr.at[sl].add(-jnp.matmul(A, coef, precision=lax.Precision.HIGHEST))
    return jnp.moveaxis(data_arr.reshape(shape), 0, axis)

