from typing import Any, Union

def concatenate(
    ar_tuple: Sequence[ArrayLike],
    axis=0,
    out: OutArray | None = None,
    dtype: DTypeLike | None = None,
    casting: CastingModes | None = "same_kind",
):
    _concat_check(ar_tuple, dtype, out=out)
    result = _concatenate(ar_tuple, axis=axis, out=out, dtype=dtype, casting=casting)
    return result


def concatenate(arrays, axis=0):
    """
    Concatenate a sequence of arrays along the given axis.

    Parameters
    ----------
    arrays : sequence of array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int, optional
        The axis along which the arrays will be joined. Default is 0.

    Returns
    -------
    result : MaskedArray
        The concatenated array with any masked entries preserved.

    See Also
    --------
    numpy.concatenate : Equivalent function in the top-level NumPy module.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> a = ma.arange(3)
    >>> a[1] = ma.masked
    >>> b = ma.arange(2, 5)
    >>> a
    masked_array(data=[0, --, 2],
                 mask=[False,  True, False],
           fill_value=999999)
    >>> b
    masked_array(data=[2, 3, 4],
                 mask=False,
           fill_value=999999)
    >>> ma.concatenate([a, b])
    masked_array(data=[0, --, 2, 2, 3, 4],
                 mask=[False,  True, False, False, False, False],
           fill_value=999999)

    """
    d = np.concatenate([getdata(a) for a in arrays], axis)
    rcls = get_masked_subclass(*arrays)
    data = d.view(rcls)
    # Check whether one of the arrays has a non-empty mask.
    for x in arrays:
        if getmask(x) is not nomask:
            break
    else:
        return data
    # OK, so we have to concatenate the masks
    dm = np.concatenate([getmaskarray(a) for a in arrays], axis)
    dm = dm.reshape(d.shape)

    # If we decide to keep a '_shrinkmask' option, we want to check that
    # all of them are True, and then check for dm.any()
    data._mask = _shrink_mask(dm)
    return data


def concatenate(arrays, axis=0, out=None, *, dtype=None, casting="same_kind"):
    """
    concatenate(
        arrays,
        /,
        axis=0,
        out=None,
        *,
        dtype=None,
        casting="same_kind",
    )
    --

    Join a sequence of arrays along an existing axis.

    .. versionadded:: 2.0
        ``numpy.concat`` added as a shorthand for ``numpy.concatenate``.

    Parameters
    ----------
    a1, a2, ... : sequence of array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int, optional
        The axis along which the arrays will be joined.  If axis is None,
        arrays are flattened before use.  Default is 0.
    out : ndarray, optional
        If provided, the destination to place the result. The shape must be
        correct, matching that of what concatenate would have returned if no
        out argument were specified.
    dtype : str or dtype
        If provided, the destination array will have this dtype. Cannot be
        provided together with `out`.

        .. versionadded:: 1.20.0

    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur. Defaults to 'same_kind'.
        For a description of the options, please see :term:`casting`.

        .. versionadded:: 1.20.0

    Returns
    -------
    res : ndarray
        The concatenated array.

    See Also
    --------
    ma.concatenate : Concatenate function that preserves input masks.
    array_split : Split an array into multiple sub-arrays of equal or
                  near-equal size.
    split : Split array into a list of multiple sub-arrays of equal size.
    hsplit : Split array into multiple sub-arrays horizontally (column wise).
    vsplit : Split array into multiple sub-arrays vertically (row wise).
    dsplit : Split array into multiple sub-arrays along the 3rd axis (depth).
    stack : Stack a sequence of arrays along a new axis.
    block : Assemble arrays from blocks.
    hstack : Stack arrays in sequence horizontally (column wise).
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).
    column_stack : Stack 1-D arrays as columns into a 2-D array.

    Notes
    -----
    When one or more of the arrays to be concatenated is a MaskedArray,
    this function will return a MaskedArray object instead of an ndarray,
    but the input masks are *not* preserved. In cases where a MaskedArray
    is expected as input, use the ma.concatenate function from the masked
    array module instead.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> b = np.array([[5, 6]])
    >>> np.concatenate((a, b), axis=0)
    array([[1, 2],
           [3, 4],
           [5, 6]])
    >>> np.concatenate((a, b.T), axis=1)
    array([[1, 2, 5],
           [3, 4, 6]])
    >>> np.concatenate((a, b), axis=None)
    array([1, 2, 3, 4, 5, 6])

    This function will not preserve masking of MaskedArray inputs.

    >>> a = np.ma.arange(3)
    >>> a[1] = np.ma.masked
    >>> b = np.arange(2, 5)
    >>> a
    masked_array(data=[0, --, 2],
                 mask=[False,  True, False],
           fill_value=999999)
    >>> b
    array([2, 3, 4])
    >>> np.concatenate([a, b])
    masked_array(data=[0, 1, 2, 2, 3, 4],
                 mask=False,
           fill_value=999999)
    >>> np.ma.concatenate([a, b])
    masked_array(data=[0, --, 2, 2, 3, 4],
                 mask=[False,  True, False, False, False, False],
           fill_value=999999)

    """
    if out is not None:
        # optimize for the typical case where only arrays is provided
        arrays = list(arrays)
        arrays.append(out)
    return arrays


def concatenate(sources: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConcatenateOp(sources=sources, dimension=dimension, results=results, loc=loc, ip=ip).result


def concatenate(val: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConcatenateOp(val=val, dimension=dimension, results=results, loc=loc, ip=ip).result


def concatenate(result: _ods_ir.Type, inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimension: _Union[_Any, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConcatenateOp(result=result, inputs=inputs, dimension=dimension, loc=loc, ip=ip).result


def concatenate(inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimension: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ConcatenateOp(inputs=inputs, dimension=dimension, results=results, loc=loc, ip=ip).result


def concatenate(operands, dimension):
  return np.concatenate(operands, axis=dimension)


def concatenate(xs: Iterable[Sequence[T]]) -> list[T]:
  """Concatenates/flattens a list of lists."""
  return list(it.chain.from_iterable(xs))


def concatenate(operands: Array | Sequence[ArrayLike], dimension: int) -> Array:
  """Concatenates a sequence of arrays along `dimension`.

  Wraps XLA's `Concatenate
  <https://www.openxla.org/xla/operation_semantics#concatenate>`_
  operator.

  Args:
    operands: a sequence of arrays to concatenate. The arrays must have equal
      shapes, except in the `dimension` axis.
    dimension: the dimension along which to concatenate the arrays.

  Returns:
    An array containing the concatenation.
  """
  if len(operands) == 0:
    raise ValueError("concatenate requires a non-empty sequences of arrays")
  if len(operands) == 1:
    op, = operands
    if isinstance(op, Array):
      return op
  operands = core.auto_insert_reshard(*operands)
  return concatenate_p.bind(*operands, dimension=dimension)


def concatenate(arrays: np.ndarray | Array | Sequence[ArrayLike],
                axis: int | None = 0, dtype: DTypeLike | None = None) -> Array:
  """Join arrays along an existing axis.

  JAX implementation of :func:`numpy.concatenate`.

  Args:
    arrays: a sequence of arrays to concatenate; each must have the same shape
      except along the specified axis. If a single array is given it will be
      treated equivalently to `arrays = unstack(arrays)`, but the implementation
      will avoid explicit unstacking.
    axis: specify the axis along which to concatenate. If None, the arrays are
      flattened before concatenation.
    dtype: optional dtype of the resulting array. If not specified, the dtype
      will be determined via type promotion rules described in :ref:`type-promotion`.

  Returns:
    the concatenated result.

  See also:
    - :func:`jax.lax.concatenate`: XLA concatenation API.
    - :func:`jax.numpy.concat`: Array API version of this function.
    - :func:`jax.numpy.stack`: concatenate arrays along a new axis.

  Examples:
    One-dimensional concatenation:

    >>> x = jnp.arange(3)
    >>> y = jnp.zeros(3, dtype=int)
    >>> jnp.concatenate([x, y])
    Array([0, 1, 2, 0, 0, 0], dtype=int32)

    Two-dimensional concatenation:

    >>> x = jnp.ones((2, 3))
    >>> y = jnp.zeros((2, 1))
    >>> jnp.concatenate([x, y], axis=1)
    Array([[1., 1., 1., 0.],
           [1., 1., 1., 0.]], dtype=float32)
  """
  if isinstance(arrays, (np.ndarray, Array)):
    return _concatenate_array(arrays, axis, dtype=dtype)
  arrays = util.ensure_arraylike_tuple("concatenate", arrays)
  if not len(arrays):
    raise ValueError("Need at least one array to concatenate.")
  if axis is None:
    return concatenate([ravel(a) for a in arrays], axis=0, dtype=dtype)
  if np.ndim(arrays[0]) == 0:
    raise ValueError("Zero-dimensional arrays cannot be concatenated.")
  axis = _canonicalize_axis(axis, np.ndim(arrays[0]))
  if dtype is None:
    arrays_out = util.promote_dtypes(*arrays)
  else:
    arrays_out = [asarray(arr, dtype=dtype) for arr in arrays]
  return lax.concatenate(arrays_out, axis)


def concatenate(
    space: Space, items: Iterable, out: tuple[Any, ...] | dict[str, Any] | np.ndarray
) -> tuple[Any, ...] | dict[str, Any] | np.ndarray:
    """Concatenate multiple samples from space into a single object.

    Args:
        space: Space of each item (e.g. `single_action_space` from vectorized environment)
        items: Samples to be concatenated (e.g. all sample should be an element of the `space`).
        out: The output object (e.g. generated from `create_empty_array`)

    Returns:
        The output object, can be the same object `out`.

    Raises:
        ValueError: Space is not a valid :class:`gymnasium.Space` instance

    Example:
        >>> from gymnasium.spaces import Box
        >>> import numpy as np
        >>> space = Box(low=0, high=1, shape=(3,), seed=42, dtype=np.float32)
        >>> out = np.zeros((2, 3), dtype=np.float32)
        >>> items = [space.sample() for _ in range(2)]
        >>> concatenate(space, items, out)
        array([[0.77395606, 0.43887845, 0.85859793],
               [0.697368  , 0.09417735, 0.97562236]], dtype=float32)
    """
    raise TypeError(
        f"The space provided to `concatenate` is not a gymnasium Space instance, type: {type(space)}, {space}"
    )


def concatenate(
    space: Space, items: Iterable, out: Union[tuple, dict, np.ndarray]
) -> Union[tuple, dict, np.ndarray]:
    """Concatenate multiple samples from space into a single object.

    Example::

        >>> from gym.spaces import Box
        >>> space = Box(low=0, high=1, shape=(3,), dtype=np.float32)
        >>> out = np.zeros((2, 3), dtype=np.float32)
        >>> items = [space.sample() for _ in range(2)]
        >>> concatenate(space, items, out)
        array([[0.6348213 , 0.28607962, 0.60760117],
               [0.87383074, 0.192658  , 0.2148103 ]], dtype=float32)

    Args:
        space: Observation space of a single environment in the vectorized environment.
        items: Samples to be concatenated.
        out: The output object. This object is a (possibly nested) numpy array.

    Returns:
        The output object. This object is a (possibly nested) numpy array.

    Raises:
        ValueError: Space is not a valid :class:`gym.Space` instance
    """
    raise ValueError(
        f"Space of type `{type(space)}` is not a valid `gym.Space` instance."
    )

