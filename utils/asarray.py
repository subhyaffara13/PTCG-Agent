
def asarray(a, dtype=None, order="K", *, like=None):
    return array(a, dtype=dtype, order=order, like=like, copy=False, ndmin=0)


def asarray(
    obj: Array | complex | NestedSequence[complex] | SupportsBufferProtocol,
    /,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    copy: py_bool | None = None,
    **kwargs: object,
) -> Array:
    """
    Array API compatibility wrapper for asarray().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    with cp.cuda.Device(device):
        if copy is None:
            return cp.asarray(obj, dtype=dtype, **kwargs)
        else:
            res = cp.array(obj, dtype=dtype, copy=copy, **kwargs)
            if not copy and res is not obj:
                raise ValueError("Unable to avoid copy while creating an array as requested")
            return res


def asarray(
    obj: Array | complex | NestedSequence[complex] | SupportsBufferProtocol,
    /,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    copy: py_bool | None = None,
    **kwargs: Any,
) -> Array:
    """
    Array API compatibility wrapper for asarray().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    _helpers._check_device(np, device)

    # None is unsupported in NumPy 1.0, but we can use an internal enum
    # False in NumPy 1.0 means None in NumPy 2.0 and in the Array API
    if copy is None:
        copy = np._CopyMode.IF_NEEDED  # type: ignore[assignment,attr-defined]
    elif copy is False:
        copy = np._CopyMode.NEVER  # type: ignore[assignment,attr-defined]

    return np.array(obj, copy=copy, dtype=dtype, **kwargs)


def asarray(
    obj: Array | complex | NestedSequence[complex] | SupportsBufferProtocol,
    /,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    copy: bool | None = None,
    **kwargs: Any,
) -> Array:
    # torch.asarray does not respect input->output device propagation
    # https://github.com/pytorch/pytorch/issues/150199
    if device is None and isinstance(obj, torch.Tensor):
        device = obj.device
    return torch.asarray(obj, dtype=dtype, device=device, copy=copy, **kwargs)


def asarray(
    obj: Array | complex | NestedSequence[complex] | SupportsBufferProtocol,
    /,
    *,
    dtype: DType | None = None,
    device: Device | None = None,
    copy: py_bool | None = None,
    **kwargs: object,
) -> Array:
    """
    Array API compatibility wrapper for asarray().

    See the corresponding documentation in the array library and/or the array API
    specification for more details.
    """
    # TODO: respect device keyword?
    _helpers._check_device(da, device)

    if isinstance(obj, da.Array):
        if dtype is not None and dtype != obj.dtype:
            if copy is False:
                raise ValueError("Unable to avoid copy when changing dtype")
            obj = obj.astype(dtype)
        return obj.copy() if copy else obj  # pyright: ignore[reportAttributeAccessIssue]

    if copy is False:
        raise ValueError(
            "Unable to avoid copy when converting a non-dask object to dask"
        )

    # copy=None to be uniform across dask < 2024.12 and >= 2024.12
    # see https://github.com/dask/dask/pull/11524/
    obj = np.array(obj, dtype=dtype, copy=True)
    return da.from_array(obj)


def asarray(a, dtype=None, order=None):
    """
    Convert the input to a masked array of the given data-type.

    No copy is performed if the input is already an `ndarray`. If `a` is
    a subclass of `MaskedArray`, a base class `MaskedArray` is returned.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to a masked array. This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists, ndarrays and masked arrays.
    dtype : dtype, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F'}, optional
        Whether to use row-major ('C') or column-major ('FORTRAN') memory
        representation.  Default is 'C'.

    Returns
    -------
    out : MaskedArray
        Masked array interpretation of `a`.

    See Also
    --------
    asanyarray : Similar to `asarray`, but conserves subclasses.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(10.).reshape(2, 5)
    >>> x
    array([[0., 1., 2., 3., 4.],
           [5., 6., 7., 8., 9.]])
    >>> np.ma.asarray(x)
    masked_array(
      data=[[0., 1., 2., 3., 4.],
            [5., 6., 7., 8., 9.]],
      mask=False,
      fill_value=1e+20)
    >>> type(np.ma.asarray(x))
    <class 'numpy.ma.MaskedArray'>

    """
    order = order or 'C'
    return masked_array(a, dtype=dtype, copy=False, keep_mask=True,
                        subok=False, order=order)


def asarray(obj, itemsize=None, unicode=None, order=None):
    """
    Convert the input to a `~numpy.char.chararray`, copying the data only if
    necessary.

    .. deprecated:: 2.5
       ``chararray`` is deprecated. Use an ``ndarray`` with a string or
       bytes dtype instead.

    Versus a NumPy array of dtype `bytes_` or `str_`, this
    class adds the following functionality:

    1) values automatically have whitespace removed from the end
       when indexed

    2) comparison operators automatically remove whitespace from the
       end when comparing values

    3) vectorized string operations are provided as methods
       (e.g. `chararray.endswith <numpy.char.chararray.endswith>`)
       and infix operators (e.g. ``+``, ``*``, ``%``)

    Parameters
    ----------
    obj : array of str or unicode-like

    itemsize : int, optional
        `itemsize` is the number of characters per scalar in the
        resulting array.  If `itemsize` is None, and `obj` is an
        object array or a Python list, the `itemsize` will be
        automatically determined.  If `itemsize` is provided and `obj`
        is of type str or unicode, then the `obj` string will be
        chunked into `itemsize` pieces.

    unicode : bool, optional
        When true, the resulting `~numpy.char.chararray` can contain Unicode
        characters, when false only 8-bit characters.  If unicode is
        None and `obj` is one of the following:

        - a `~numpy.char.chararray`,
        - an ndarray of type `str_` or `unicode_`
        - a Python str or unicode object,

        then the unicode setting of the output array will be
        automatically determined.

    order : {'C', 'F'}, optional
        Specify the order of the array.  If order is 'C' (default), then the
        array will be in C-contiguous order (last-index varies the
        fastest).  If order is 'F', then the returned array
        will be in Fortran-contiguous order (first-index varies the
        fastest).

    Examples
    --------
    >>> import numpy as np
    >>> np.char.asarray(['hello', 'world'])
    chararray(['hello', 'world'], dtype='<U5')

    """
    return array(obj, itemsize, copy=False,
                 unicode=unicode, order=order)


def asarray(x: ArrayLike) -> Array:
  """Lightweight conversion of ArrayLike input to Array output."""
  if isinstance(x, Array):
    return x
  elif isinstance(x, literals.TypedNdArray):
    return _convert_element_type(x, weak_type=x.weak_type)
  elif isinstance(x, (bool, np.ndarray, np.generic)):
    return _convert_element_type(x, weak_type=False)
  elif isinstance(x, (int, float, builtins.complex)):
    return _convert_element_type(dtypes.coerce_to_array(x), weak_type=True)
  else:
    raise TypeError(f"asarray: expected ArrayLike, got {x} of type {type(x)}.")


def asarray(a: Any, dtype: DTypeLike | None = None, order: str | None = None,
            *, copy: bool | None = None,
            device: xc.Device | Sharding | None = None,
            out_sharding: NamedSharding | P | None = None) -> Array:
  """Convert an object to a JAX array.

  JAX implementation of :func:`numpy.asarray`.

  Args:
    a: an object that is convertible to an array. This includes JAX
      arrays, NumPy arrays, Python scalars, Python collections like lists
      and tuples, objects with a ``__jax_array__`` method, and objects
      supporting the Python buffer protocol.
    dtype: optionally specify the dtype of the output array. If not
      specified it will be inferred from the input.
    order: not implemented in JAX
    copy: optional boolean specifying the copy mode. If True, then always
      return a copy. If False, then error if a copy is necessary. Default is
      None, which will only copy when necessary.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    A JAX array constructed from the input.

  See also:
    - :func:`jax.numpy.array`: like `asarray`, but defaults to `copy=True`.
    - :func:`jax.numpy.from_dlpack`: construct a JAX array from an object
      that implements the dlpack interface.
    - :func:`jax.numpy.frombuffer`: construct a JAX array from an object
      that implements the buffer interface.

  Examples:
    Constructing JAX arrays from Python scalars:

    >>> jnp.asarray(True)
    Array(True, dtype=bool)
    >>> jnp.asarray(42)
    Array(42, dtype=int32, weak_type=True)
    >>> jnp.asarray(3.5)
    Array(3.5, dtype=float32, weak_type=True)
    >>> jnp.asarray(1 + 1j)
    Array(1.+1.j, dtype=complex64, weak_type=True)

    Constructing JAX arrays from Python collections:

    >>> jnp.asarray([1, 2, 3])  # list of ints -> 1D array
    Array([1, 2, 3], dtype=int32)
    >>> jnp.asarray([(1, 2, 3), (4, 5, 6)])  # list of tuples of ints -> 2D array
    Array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)
    >>> jnp.asarray(range(5))
    Array([0, 1, 2, 3, 4], dtype=int32)

    Constructing JAX arrays from NumPy arrays:

    >>> jnp.asarray(np.linspace(0, 2, 5))
    Array([0. , 0.5, 1. , 1.5, 2. ], dtype=float32)

    Constructing a JAX array via the Python buffer interface, using Python's
    built-in :mod:`array` module.

    >>> from array import array
    >>> pybuffer = array('i', [2, 3, 5, 7])
    >>> jnp.asarray(pybuffer)
    Array([2, 3, 5, 7], dtype=int32)
  """
  # For copy=False, the array API specifies that we raise a ValueError if the input supports
  # the buffer protocol but a copy is required. Since array() supports the buffer protocol
  # via numpy, this is only the case when the default device is not 'cpu'
  if (copy is False and not isinstance(a, Array)
      and _get_platform(device) != "cpu"
      and _supports_buffer_protocol(a)):
    raise ValueError(f"jnp.asarray: cannot convert object of type {type(a)} to JAX Array "
                     f"on platform={_get_platform(device)} with "
                     "copy=False. Consider using copy=None or copy=True instead.")
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "asarray")
  return array(a, dtype=dtype, copy=bool(copy), order=order, device=device,
               out_sharding=out_sharding)

