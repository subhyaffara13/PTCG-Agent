import copy

def reshape(array, newshape):
    """
    Framework-agnostic version of reshape operation.
    """
    if is_numpy_array(array):
        return np.reshape(array, newshape)
    elif is_torch_tensor(array):
        return array.reshape(*newshape)
    else:
        raise ValueError(f"Type not supported for reshape: {type(array)}.")


def reshape(a: ArrayLike, newshape, order: NotImplementedType = "C"):
    # if sh = (1, 2, 3), numpy allows both .reshape(sh) and .reshape(*sh)
    newshape = newshape[0] if len(newshape) == 1 else newshape
    return a.reshape(newshape)


def reshape(a: TensorLikeType, *shape: ShapeType) -> TensorLikeType:
    return _reshape_view_helper(a, *shape, allow_copy=True)


def reshape(g: jit_utils.GraphContext, self, shape):
    # NOTE: Due to bug in ORT https://github.com/microsoft/onnxruntime/issues/10664
    #       Reshape export cannot utilize the new allowzero attribute introduced in opset 14.
    return symbolic_helper._reshape_helper(g, self, shape, allowzero=0)


def reshape(g: jit_utils.GraphContext, self, shape):
    return symbolic_helper._reshape_helper(g, self, shape)


def reshape(source, shape, pad=None, order=None):
    """ Creates an AST node for a function call to Fortran's "reshape(...)"

    Parameters
    ==========

    source : Symbol or String
    shape : ArrayExpr

    """
    return FunctionCall(
        'reshape',
        [_printable(source), _printable(shape)] +
        ([_printable(pad)] if pad else []) +
        ([_printable(order)] if pad else [])
    )


def reshape(seq, how):
    """Reshape the sequence according to the template in ``how``.

    Examples
    ========

    >>> from sympy.utilities import reshape
    >>> seq = list(range(1, 9))

    >>> reshape(seq, [4]) # lists of 4
    [[1, 2, 3, 4], [5, 6, 7, 8]]

    >>> reshape(seq, (4,)) # tuples of 4
    [(1, 2, 3, 4), (5, 6, 7, 8)]

    >>> reshape(seq, (2, 2)) # tuples of 4
    [(1, 2, 3, 4), (5, 6, 7, 8)]

    >>> reshape(seq, (2, [2])) # (i, i, [i, i])
    [(1, 2, [3, 4]), (5, 6, [7, 8])]

    >>> reshape(seq, ((2,), [2])) # etc....
    [((1, 2), [3, 4]), ((5, 6), [7, 8])]

    >>> reshape(seq, (1, [2], 1))
    [(1, [2, 3], 4), (5, [6, 7], 8)]

    >>> reshape(tuple(seq), ([[1], 1, (2,)],))
    (([[1], 2, (3, 4)],), ([[5], 6, (7, 8)],))

    >>> reshape(tuple(seq), ([1], 1, (2,)))
    (([1], 2, (3, 4)), ([5], 6, (7, 8)))

    >>> reshape(list(range(12)), [2, [3], {2}, (1, (3,), 1)])
    [[0, 1, [2, 3, 4], {5, 6}, (7, (8, 9, 10), 11)]]

    """
    m = sum(flatten(how))
    n, rem = divmod(len(seq), m)
    if m < 0 or rem:
        raise ValueError('template must sum to positive number '
        'that divides the length of the sequence')
    i = 0
    container = type(how)
    rv = [None]*n
    for k in range(len(rv)):
        _rv = []
        for hi in how:
            if isinstance(hi, int):
                _rv.extend(seq[i: i + hi])
                i += hi
            else:
                n = sum(flatten(hi))
                hi_type = type(hi)
                _rv.append(hi_type(reshape(seq[i: i + n], hi)[0]))
                i += n
        rv[k] = container(_rv)
    return type(seq)(rv)


def reshape(matrix, shape):
    """Change the shape of a *matrix*.

    If *shape* is an integer, the matrix must be two dimensional
    and the shape is interpreted as the desired number of columns:

        >>> matrix = [(0, 1), (2, 3), (4, 5)]
        >>> cols = 3
        >>> list(reshape(matrix, cols))
        [(0, 1, 2), (3, 4, 5)]

    If *shape* is a tuple (or other iterable), the input matrix can have
    any number of dimensions. It will first be flattened and then rebuilt
    to the desired shape which can also be multidimensional:

        >>> matrix = [(0, 1), (2, 3), (4, 5)]    # Start with a 3 x 2 matrix

        >>> list(reshape(matrix, (2, 3)))        # Make a 2 x 3 matrix
        [(0, 1, 2), (3, 4, 5)]

        >>> list(reshape(matrix, (6,)))          # Make a vector of length six
        [0, 1, 2, 3, 4, 5]

        >>> list(reshape(matrix, (2, 1, 3, 1)))  # Make 2 x 1 x 3 x 1 tensor
        [(((0,), (1,), (2,)),), (((3,), (4,), (5,)),)]

    Each dimension is assumed to be uniform, either all arrays or all scalars.
    Flattening stops when the first value in a dimension is a scalar.
    Scalars are bytes, strings, and non-iterables.
    The reshape iterator stops when the requested shape is complete
    or when the input is exhausted, whichever comes first.

    """
    if isinstance(shape, int):
        return batched(chain.from_iterable(matrix), shape)
    first_dim, *dims = shape
    scalar_stream = _flatten_tensor(matrix)
    reshaped = reduce(batched, reversed(dims), scalar_stream)
    return islice(reshaped, first_dim)


def reshape(
    x: Array,
    /,
    shape: tuple[int, ...],
    xp: Namespace,
    *,
    copy: bool | None = None,
    **kwargs: object,
) -> Array:
    if copy is True:
        x = x.copy()
    elif copy is False:
        y = x.view()
        y.shape = shape
        return y
    return xp.reshape(x, shape, **kwargs)


def reshape(x: Array,
            /,
            shape: tuple[int, ...],
            *,
            copy: bool | None = None,
            **kwargs: object) -> Array:
    if copy is not None:
        raise NotImplementedError("torch.reshape doesn't yet support the copy keyword")
    return torch.reshape(x, shape, **kwargs)


def reshape(a, new_shape, order='C'):
    """
    Returns an array containing the same data with a new shape.

    Refer to `MaskedArray.reshape` for full documentation.

    See Also
    --------
    MaskedArray.reshape : equivalent function

    Examples
    --------
    Reshaping a 1-D array:

    >>> a = np.ma.array([1, 2, 3, 4])
    >>> np.ma.reshape(a, (2, 2))
    masked_array(
      data=[[1, 2],
            [3, 4]],
      mask=False,
      fill_value=999999)

    Reshaping a 2-D array:

    >>> b = np.ma.array([[1, 2], [3, 4]])
    >>> np.ma.reshape(b, (1, 4))
    masked_array(data=[[1, 2, 3, 4]],
                 mask=False,
           fill_value=999999)

    Reshaping a 1-D array with a mask:

    >>> c = np.ma.array([1, 2, 3, 4], mask=[False, True, False, False])
    >>> np.ma.reshape(c, (2, 2))
    masked_array(
      data=[[1, --],
            [3, 4]],
      mask=[[False,  True],
            [False, False]],
      fill_value=999999)

    """
    # We can't use 'frommethod', it whine about some parameters. Dmmit.
    try:
        return a.reshape(new_shape, order=order)
    except AttributeError:
        _tmp = np.asarray(a).reshape(new_shape, order=order)
        return _tmp.view(MaskedArray)


def reshape(a, /, shape, order='C', *, copy=None):
    """
    Returns a reshaped ndarray without changing data.

    Parameters
    ----------
    a : array_like
        Array to be reshaped.
    shape : int or tuple of ints
        The new shape should be compatible with the original shape. If
        an integer, then the result will be a 1-D array of that length.
        One shape dimension can be -1. In this case, the value is
        inferred from the length of the array and remaining dimensions.
    order : {'C', 'F', 'A'}, optional
        Read the elements of ``a`` using this index order, and place the
        elements into the reshaped array using this index order. 'C'
        means to read / write the elements using C-like index order,
        with the last axis index changing fastest, back to the first
        axis index changing slowest. 'F' means to read / write the
        elements using Fortran-like index order, with the first index
        changing fastest, and the last index changing slowest. Note that
        the 'C' and 'F' options take no account of the memory layout of
        the underlying array, and only refer to the order of indexing.
        'A' means to read / write the elements in Fortran-like index
        order if ``a`` is Fortran *contiguous* in memory, C-like order
        otherwise.
    copy : bool, optional
        If ``True``, then the array data is copied. If ``None``, a copy will
        only be made if it's required by ``order``. For ``False`` it raises
        a ``ValueError`` if a copy cannot be avoided. Default: ``None``.

    Returns
    -------
    reshaped_array : ndarray
        This will be a new view object if possible; otherwise, it will
        be a copy.  Note there is no guarantee of the *memory layout* (C- or
        Fortran- contiguous) of the returned array.

    See Also
    --------
    ndarray.reshape : Equivalent method.

    Notes
    -----
    It is not always possible to change the shape of an array without copying
    the data.

    The ``order`` keyword gives the index ordering both for *fetching*
    the values from ``a``, and then *placing* the values into the output
    array. For example, let's say you have an array:

    >>> a = np.arange(6).reshape((3, 2))
    >>> a
    array([[0, 1],
           [2, 3],
           [4, 5]])

    You can think of reshaping as first raveling the array (using the given
    index order), then inserting the elements from the raveled array into the
    new array using the same kind of index ordering as was used for the
    raveling.

    >>> np.reshape(a, (2, 3)) # C-like index ordering
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.reshape(np.ravel(a), (2, 3)) # equivalent to C ravel then C reshape
    array([[0, 1, 2],
           [3, 4, 5]])
    >>> np.reshape(a, (2, 3), order='F') # Fortran-like index ordering
    array([[0, 4, 3],
           [2, 1, 5]])
    >>> np.reshape(np.ravel(a, order='F'), (2, 3), order='F')
    array([[0, 4, 3],
           [2, 1, 5]])

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1,2,3], [4,5,6]])
    >>> np.reshape(a, 6)
    array([1, 2, 3, 4, 5, 6])
    >>> np.reshape(a, 6, order='F')
    array([1, 4, 2, 5, 3, 6])

    >>> np.reshape(a, (3,-1))       # the unspecified value is inferred to be 2
    array([[1, 2],
           [3, 4],
           [5, 6]])
    """
    if copy is not None:
        return _wrapfunc(a, 'reshape', shape, order=order, copy=copy)
    return _wrapfunc(a, 'reshape', shape, order=order)


def reshape(result: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.RankedTensorType], *, allow_reorder: _Optional[bool] = None, efficient_layout: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReshapeOp(result=result, src=src, allow_reorder=allow_reorder, efficient_layout=efficient_layout, loc=loc, ip=ip).result


def reshape(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ReshapeOp(result=result, source=source, loc=loc, ip=ip).result


def reshape(result: _ods_ir.Type, source: _ods_ir.Value, shape: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReshapeOp(result=result, source=source, shape=shape, loc=loc, ip=ip).result


def reshape(result: _ods_ir.Type, operand: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReshapeOp(result=result, operand=operand, loc=loc, ip=ip).result


def reshape(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReshapeOp(result=result, operand=operand, loc=loc, ip=ip).result


def reshape(operand, new_sizes, dimensions=None):
  if dimensions is None:
    dimensions = range(len(np.shape(operand)))
  return np.reshape(np.transpose(operand, dimensions), new_sizes)


def reshape(ctx: LoweringRuleContext, op, aval_out: core.AbstractValue) -> ir.Value:
  aval_out = core.physical_aval(aval_out)
  if not core.is_constant_shape(aval_out.shape):  # pyrefly: ignore[missing-attribute]
    shape = eval_dynamic_shape_as_tensor(ctx, aval_out.shape)  # pyrefly: ignore[missing-attribute]
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.dynamic_reshape(
        result_type, op, shape,
    )
  else:
    (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
    return hlo.reshape(result_type, op)


def reshape(operand: ArrayLike, new_sizes: Shape,
            dimensions: Sequence[int] | None = None,
            *, out_sharding: NamedSharding | P | None = None) -> Array:
  """Wraps XLA's `Reshape
  <https://www.openxla.org/xla/operation_semantics#reshape>`_
  operator.

  For inserting/removing dimensions of size 1, prefer using ``lax.squeeze`` /
  ``lax.expand_dims``. These preserve information about axis identity that may
  be useful for advanced transformation rules.

  Args:
    operand: array to be reshaped.
    new_sizes: sequence of integers specifying the resulting shape. The size
      of the final array must match the size of the input.
    dimensions: optional sequence of integers specifying the permutation order of
      the input shape. If specified, the length must match ``operand.shape``.

  Returns:
    out: reshaped array.

  Examples:
    Simple reshaping from one to two dimensions:

    >>> x = jnp.arange(6)
    >>> y = reshape(x, (2, 3))
    >>> y
    Array([[0, 1, 2],
                 [3, 4, 5]], dtype=int32)

    Reshaping back to one dimension:

    >>> reshape(y, (6,))
    Array([0, 1, 2, 3, 4, 5], dtype=int32)

    Reshaping to one dimension with permutation of dimensions:

    >>> reshape(y, (6,), (1, 0))
    Array([0, 3, 1, 4, 2, 5], dtype=int32)
  """
  new_sizes = canonicalize_shape(new_sizes)
  new_sizes = tuple(new_sizes)
  same_shape = core.definitely_equal_shape(np.shape(operand), new_sizes)
  if dimensions is None:
    same_dims = True
    dims = None
  else:
    dims = api_util._ensure_index_tuple(dimensions)
    same_dims = tuple(dims) == tuple(range(np.ndim(operand)))
  out_sharding = canonicalize_sharding(out_sharding, 'reshape')
  same_sharding = (out_sharding is None or
                   typeof(operand).sharding == out_sharding)

  if (np.shape(operand) and same_shape and same_dims and same_sharding and
      isinstance(operand, Array)):
    return operand
  else:
    return reshape_p.bind(
      operand, new_sizes=new_sizes,
      dimensions=None if dims is None or same_dims else dims,
      sharding=out_sharding)


def reshape(
    a: ArrayLike, shape: DimSize | Shape, order: str = "C", *,
    copy: bool | None = None, out_sharding=None) -> Array:
  """Return a reshaped copy of an array.

  JAX implementation of :func:`numpy.reshape`, implemented in terms of
  :func:`jax.lax.reshape`.

  Args:
    a: input array to reshape
    shape: integer or sequence of integers giving the new shape, which must match the
      size of the input array. If any single dimension is given size ``-1``, it will be
      replaced with a value such that the output has the correct size.
    order: ``'F'`` or ``'C'``, specifies whether the reshape should apply column-major
      (fortran-style, ``"F"``) or row-major (C-style, ``"C"``) order; default is ``"C"``.
      JAX does not support ``order="A"``.
    copy: unused by JAX; JAX always returns a copy, though under JIT the compiler
      may optimize such copies away.

  Returns:
    reshaped copy of input array with the specified shape.

  Notes:
    Unlike :func:`numpy.reshape`, :func:`jax.numpy.reshape` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :meth:`jax.Array.reshape`: equivalent functionality via an array method.
    - :func:`jax.numpy.ravel`: flatten an array into a 1D shape.
    - :func:`jax.numpy.squeeze`: remove one or more length-1 axes from an array's shape.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.reshape(x, 6)
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
    >>> jnp.reshape(x, (3, 2))
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    You can use ``-1`` to automatically compute a shape that is consistent with
    the input size:

    >>> jnp.reshape(x, -1)  # -1 is inferred to be 6
    Array([1, 2, 3, 4, 5, 6], dtype=int32)
    >>> jnp.reshape(x, (-1, 2))  # -1 is inferred to be 3
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)

    The default ordering of axes in the reshape is C-style row-major ordering.
    To use Fortran-style column-major ordering, specify ``order='F'``:

    >>> jnp.reshape(x, 6, order='F')
    Array([1, 4, 2, 5, 3, 6], dtype=int32)
    >>> jnp.reshape(x, (3, 2), order='F')
    Array([[1, 5],
           [4, 3],
           [2, 6]], dtype=int32)

    For convenience, this functionality is also available via the
    :meth:`jax.Array.reshape` method:

    >>> x.reshape(3, 2)
    Array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)
  """
  del copy  # unused

  __tracebackhide__ = True
  util.check_arraylike("reshape", a)

  try:
    if out_sharding is None:
      # forward to method for ndarrays
      return a.reshape(shape, order=order)  # pyrefly: ignore[missing-attribute]
  except AttributeError:
    pass
  return asarray(a).reshape(shape, order=order, out_sharding=out_sharding)

