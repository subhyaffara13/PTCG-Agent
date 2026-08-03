import copy

def astype(
    x: Array,
    dtype: DType,
    /,
    *,
    copy: py_bool = True,
    device: Device | None = None,
) -> Array:
    if device is None:
        return x.astype(dtype=dtype, copy=copy)
    out = _helpers.to_device(x.astype(dtype=dtype, copy=False), device)
    return out.copy() if copy and out is x else out


def astype(
    x: Array,
    dtype: DType,
    /,
    *,
    copy: py_bool = True,
    device: Device | None = None,
) -> Array:
    _helpers._check_device(np, device)
    return x.astype(dtype=dtype, copy=copy)


def astype(
    x: Array,
    dtype: DType,
    /,
    *,
    copy: bool = True,
    device: Device | None = None,
) -> Array:
    if device is not None:
        return x.to(device, dtype=dtype, copy=copy)
    return x.to(dtype=dtype, copy=copy)


def astype(
    x: Array,
    dtype: DType,
    /,
    *,
    copy: py_bool = True,
    device: Device | None = None,
) -> Array:
    """
    Array API compatibility wrapper for astype().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    # TODO: respect device keyword?
    _helpers._check_device(da, device)

    if not copy and dtype == x.dtype:
        return x
    x = x.astype(dtype)
    return x.copy() if copy else x


def astype(x, dtype, /, *, copy=True, device=None):
    """
    Copies an array to a specified data type.

    This function is an Array API compatible alternative to
    `numpy.ndarray.astype`.

    Parameters
    ----------
    x : ndarray
        Input NumPy array to cast. ``array_likes`` are explicitly not
        supported here.
    dtype : dtype
        Data type of the result.
    copy : bool, optional
        Specifies whether to copy an array when the specified dtype matches
        the data type of the input array ``x``. If ``True``, a newly allocated
        array must always be returned. If ``False`` and the specified dtype
        matches the data type of the input array, the input array must be
        returned; otherwise, a newly allocated array must be returned.
        Defaults to ``True``.
    device : str, optional
        The device on which to place the returned array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.1.0

    Returns
    -------
    out : ndarray
        An array having the specified data type.

    See Also
    --------
    ndarray.astype

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.array([1, 2, 3]); arr
    array([1, 2, 3])
    >>> np.astype(arr, np.float64)
    array([1., 2., 3.])

    Non-copy case:

    >>> arr = np.array([1, 2, 3])
    >>> arr_noncpy = np.astype(arr, arr.dtype, copy=False)
    >>> np.shares_memory(arr, arr_noncpy)
    True

    """
    if not (isinstance(x, np.ndarray) or isscalar(x)):
        raise TypeError(
            "Input should be a NumPy array or scalar. "
            f"It is a {type(x)} instead."
        )
    if device is not None and device != "cpu":
        raise ValueError(
            'Device not understood. Only "cpu" is allowed, but received:'
            f' {device}'
        )
    return x.astype(dtype, copy=copy)


def astype(x: ArrayLike, dtype: DTypeLike | None,
           /, *, copy: bool = False,
           device: xc.Device | Sharding | None = None) -> Array:
  """Convert an array to a specified dtype.

  JAX implementation of :func:`numpy.astype`.

  This is implemented via :func:`jax.lax.convert_element_type`, which may
  have slightly different behavior than :func:`numpy.astype` in some cases.
  In particular, the details of float-to-int and int-to-float casts are
  implementation dependent.

  Args:
    x: input array to convert
    dtype: output dtype
    copy: if True, then always return a copy. If False (default) then only
      return a copy if necessary.
    device: optionally specify the device to which the output will be committed.

  Returns:
    An array with the same shape as ``x``, containing values of the specified
    dtype.

  See Also:
    - :func:`jax.lax.convert_element_type`: lower-level function for XLA-style
      dtype conversions.

  Examples:
    >>> x = jnp.array([0, 1, 2, 3])
    >>> x
    Array([0, 1, 2, 3], dtype=int32)
    >>> x.astype('float32')
    Array([0.0, 1.0, 2.0, 3.0], dtype=float32)

    >>> y = jnp.array([0.0, 0.5, 1.0])
    >>> y.astype(int)  # truncates fractional values
    Array([0, 0, 1], dtype=int32)
  """
  x_arr = util.ensure_arraylike("astype", x)

  if dtype is None:
    dtype = dtypes.default_float_dtype()
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "astype")
  if issubdtype(x_arr.dtype, np.complexfloating):
    if dtypes.isdtype(dtype, ("integral", "real floating")):
      deprecations.warn(
        "jax-numpy-astype-complex-to-real",
        "Casting from complex to real dtypes will soon raise a ValueError. "
        "Please first use jnp.real or jnp.imag to take the real/imaginary "
        "component of your input.",
        stacklevel=2)
    elif np.dtype(dtype) == bool:
      # convert_element_type(complex, bool) has the wrong semantics.
      x_arr = (x_arr != lax._const(x_arr, 0))

  # We offer a more specific warning than the usual ComplexWarning so we prefer
  # to issue our warning.
  result = lax._convert_element_type(
    x_arr, dtype, sharding=util.canonicalize_device_to_sharding(device),
    warn_on_complex_to_real_cast=False)
  return lax._array_copy(result) if copy else result


def astype(x: Array['*d'], dtype) -> Array['*d']:
  """`x.astype(dtype)`."""
  if lazy.is_torch(x):
    return x.type(dtype)
  elif lazy.is_tf(x):
    return lazy.tf.cast(x, dtype)
  else:
    return x.astype(dtype)

