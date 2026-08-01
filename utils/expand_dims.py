
def expand_dims(array, axis):
    """
    Framework-agnostic version of expand_dims operation.
    """
    if is_numpy_array(array):
        return np.expand_dims(array, axis)
    elif is_torch_tensor(array):
        return array.unsqueeze(dim=axis)
    else:
        raise ValueError(f"Type not supported for expand_dims: {type(array)}.")


def expand_dims(a: ArrayLike, axis):
    shape = _util.expand_shape(a.shape, axis)
    return a.view(shape)  # never copies


def expand_dims(
    a: TensorLikeType, dimensions: DimsSequenceType, ndim=None
) -> TensorLikeType:
    """
    Creates a view of a with a.ndim + len(dimensions) dimensions, with new
    dimensions of length one at the dimensions specified by dimensions.
    """
    if ndim is not None:
        # TODO: this is only here to support the unsqueeze ref
        dims = sorted(utils.canonicalize_dims(ndim, dimensions))  # type: ignore[arg-type]
    else:
        dims = sorted(utils.canonicalize_dims(a.ndim, dimensions))  # type: ignore[arg-type]
    if len(set(dims)) != len(dims):
        msg = f"Received duplicate dimensions to expand in {str(dimensions)}"
        raise ValueError(msg)

    new_shape = list(a.shape)
    for idx in dims:
        new_shape.insert(idx, 1)

    broadcast_dimensions = [
        idx for idx in range(len(new_shape)) if idx not in dimensions
    ]
    return broadcast_in_dim(a, new_shape, broadcast_dimensions)


def expand_dims(A, /, *, axis=0):
    """
    Add trivial axes to an array. Shape gets a ``1`` inserted at position `axis`.

    Parameters
    ----------
    A : sparse array
        Input array.
    axis : int
        Position in the expanded axes where the new axis (or axes) is placed.
        For a dimension ``N`` array, a valid axis is an integer on the
        closed-interval ``[-N-1, N]``. Negative values work from the end of
        the shape. ``0`` prepends an axis, as does ``-N-1``. ``-1`` appends
        an axis, as does ``N``. The new axis has shape ``1`` and indices are
        created with the value ``0``.

    Returns
    -------
    out : sparse array
        An expanded copy output in COO format with the same dtype as `A`.

    Raises
    ------
    ValueError
        If provided a non-integer or out of range ``[-N-1, N]`` axis,
        where ``N`` is ``A.ndim``.

    Examples
    --------
    >>> from scipy.sparse import csr_array, expand_dims
    >>> A = csr_array([[1, 2], [2, 0]])
    >>> A.shape
    (2, 2)
    >>> expand_dims(A, axis=1).shape
    (2, 1, 2)

    """
    if not isintlike(axis):
        raise ValueError(f"Invalid axis {axis}. Must be an integer.")
    idx = axis if axis >= 0 else axis + A.ndim + 1
    if idx < 0 or idx > A.ndim:
        raise ValueError(f"Invalid axis {axis} for N={A.ndim}. Must be in [-N-1, N].")

    newA = A.tocoo(copy=True)
    new_coord = np.zeros_like(newA.coords[0])

    newA.coords = newA.coords[:idx] + (new_coord,) + newA.coords[idx:]
    newA._shape = newA.shape[:idx] + (1,) + newA.shape[idx:]
    if A.format == "coo":
        newA.has_canonical_format = A.has_canonical_format
    return newA


def expand_dims(
    a: Array, /, *, axis: int | tuple[int, ...] = (0,), xp: ModuleType | None = None
) -> Array:
    """
    Expand the shape of an array.

    Insert (a) new axis/axes that will appear at the position(s) specified by
    `axis` in the expanded array shape.

    This is ``xp.expand_dims`` for `axis` an int *or a tuple of ints*.
    Roughly equivalent to ``numpy.expand_dims`` for NumPy arrays.

    Parameters
    ----------
    a : array
        Array to have its shape expanded.
    axis : int or tuple of ints, optional
        Position(s) in the expanded axes where the new axis (or axes) is/are placed.
        If multiple positions are provided, they should be unique (note that a position
        given by a positive index could also be referred to by a negative index -
        that will also result in an error).
        Default: ``(0,)``.
    xp : array_namespace, optional
        The standard-compatible namespace for `a`. Default: infer.

    Returns
    -------
    array
        `a` with an expanded shape.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> x = xp.asarray([1, 2])
    >>> x.shape
    (2,)

    The following is equivalent to ``x[xp.newaxis, :]`` or ``x[xp.newaxis]``:

    >>> y = xpx.expand_dims(x, axis=0, xp=xp)
    >>> y
    Array([[1, 2]], dtype=array_api_strict.int64)
    >>> y.shape
    (1, 2)

    The following is equivalent to ``x[:, xp.newaxis]``:

    >>> y = xpx.expand_dims(x, axis=1, xp=xp)
    >>> y
    Array([[1],
           [2]], dtype=array_api_strict.int64)
    >>> y.shape
    (2, 1)

    ``axis`` may also be a tuple:

    >>> y = xpx.expand_dims(x, axis=(0, 1), xp=xp)
    >>> y
    Array([[[1, 2]]], dtype=array_api_strict.int64)

    >>> y = xpx.expand_dims(x, axis=(2, 0), xp=xp)
    >>> y
    Array([[[1],
            [2]]], dtype=array_api_strict.int64)
    """
    if xp is None:
        xp = array_namespace(a)

    if not isinstance(axis, tuple):
        axis = (axis,)
    ndim = a.ndim + len(axis)
    if axis != () and (min(axis) < -ndim or max(axis) >= ndim):
        err_msg = (
            f"a provided axis position is out of bounds for array of dimension {a.ndim}"
        )
        raise IndexError(err_msg)
    axis = tuple(dim % ndim for dim in axis)
    if len(set(axis)) != len(axis):
        err_msg = "Duplicate dimensions specified in `axis`."
        raise ValueError(err_msg)

    if is_numpy_namespace(xp) or is_dask_namespace(xp) or is_jax_namespace(xp):
        return xp.expand_dims(a, axis=axis)

    return _funcs.expand_dims(a, axis=axis, xp=xp)


def expand_dims(a: Array, /, *, axis: tuple[int, ...] = (0,), xp: ModuleType) -> Array:
    # numpydoc ignore=PR01,RT01
    """See docstring in array_api_extra._delegation."""
    for i in sorted(axis):
        a = xp.expand_dims(a, axis=i)
    return a


def expand_dims(x: Array, /, axis: int | tuple[int, ...]) -> Array:
    if isinstance(axis, int):
        return torch.unsqueeze(x, axis)
    else:
        # follow https://github.com/numpy/numpy/blob/maintenance/2.4.x/numpy/lib/_shape_base_impl.py#L596-L602
        y_ndim = x.ndim + len(axis)

        # normalize
        n_axis = tuple(ax + y_ndim if ax < 0 else ax for ax in axis)
        if (len(n_axis) != len(set(n_axis)) or
            _builtin_any(ax < 0 or ax >= y_ndim for ax in n_axis)
        ):
            raise ValueError(f"{axis=} not allowed for {x.shape = }")

        shape_it = iter(x.shape)
        shape = [1 if ax in n_axis else next(shape_it) for ax in range(y_ndim)]

        return torch.reshape(x, shape)


def expand_dims(a, axis):
    """
    Expand the shape of an array.

    Insert a new axis that will appear at the `axis` position in the expanded
    array shape.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int or tuple of ints
        Position in the expanded axes where the new axis (or axes) is placed.

        .. deprecated:: 1.13.0
            Passing an axis where ``axis > a.ndim`` will be treated as
            ``axis == a.ndim``, and passing ``axis < -a.ndim - 1`` will
            be treated as ``axis == 0``. This behavior is deprecated.

    Returns
    -------
    result : ndarray
        View of `a` with the number of dimensions increased.

    See Also
    --------
    squeeze : The inverse operation, removing singleton dimensions
    reshape : Insert, remove, and combine dimensions, and resize existing ones
    atleast_1d, atleast_2d, atleast_3d

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2])
    >>> x.shape
    (2,)

    The following is equivalent to ``x[np.newaxis, :]`` or ``x[np.newaxis]``:

    >>> y = np.expand_dims(x, axis=0)
    >>> y
    array([[1, 2]])
    >>> y.shape
    (1, 2)

    The following is equivalent to ``x[:, np.newaxis]``:

    >>> y = np.expand_dims(x, axis=1)
    >>> y
    array([[1],
           [2]])
    >>> y.shape
    (2, 1)

    ``axis`` may also be a tuple:

    >>> y = np.expand_dims(x, axis=(0, 1))
    >>> y
    array([[[1, 2]]])

    >>> y = np.expand_dims(x, axis=(2, 0))
    >>> y
    array([[[1],
            [2]]])

    Note that some examples may use ``None`` instead of ``np.newaxis``.  These
    are the same objects:

    >>> np.newaxis is None
    True

    """
    if isinstance(a, matrix):
        a = asarray(a)
    else:
        a = asanyarray(a)

    if not isinstance(axis, (tuple, list)):
        axis = (axis,)

    out_ndim = len(axis) + a.ndim
    axis = normalize_axis_tuple(axis, out_ndim)

    shape_it = iter(a.shape)
    shape = [1 if ax in axis else next(shape_it) for ax in range(out_ndim)]

    return a.reshape(shape)


def expand_dims(src: _ods_ir.Value[_ods_ir.RankedTensorType], axis: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ExpandDimsOp(src=src, axis=axis, results=results, loc=loc, ip=ip).result


def expand_dims(array: ArrayLike, dimensions: Sequence[int]) -> Array:
  """Insert any number of size 1 dimensions into an array."""
  if len(set(dimensions)) != len(dimensions):
    raise ValueError(f'repeated axis in lax.expand_dims: {dimensions}')
  ndim_out = np.ndim(array) + len(dimensions)
  dims = [canonicalize_axis(i, ndim_out) for i in dimensions]
  if len(set(dims)) != len(dims):  # check again after canonicalizing
    raise ValueError(f'repeated axis in lax.expand_dims: {dims}')
  dims_set = frozenset(dims)
  result_shape = list(np.shape(array))
  for i in sorted(dims_set):
    result_shape.insert(i, 1)
  broadcast_dims = [i for i in range(ndim_out) if i not in dims_set]
  return broadcast_in_dim(array, result_shape, broadcast_dims)


def expand_dims(a: ArrayLike, axis: int | Sequence[int]) -> Array:
  """Insert dimensions of length 1 into array

  JAX implementation of :func:`numpy.expand_dims`, implemented via
  :func:`jax.lax.expand_dims`.

  Args:
    a: input array
    axis: integer or sequence of integers specifying positions of axes to add.

  Returns:
    Copy of ``a`` with added dimensions.

  Notes:
    Unlike :func:`numpy.expand_dims`, :func:`jax.numpy.expand_dims` will return a copy
    rather than a view of the input array. However, under JIT, the compiler will optimize
    away such copies when possible, so this doesn't have performance impacts in practice.

  See Also:
    - :func:`jax.numpy.squeeze`: inverse of this operation, i.e. remove length-1 dimensions.
    - :func:`jax.lax.expand_dims`: XLA version of this functionality.

  Examples:
    >>> x = jnp.array([1, 2, 3])
    >>> x.shape
    (3,)

    Expand the leading dimension:

    >>> jnp.expand_dims(x, 0)
    Array([[1, 2, 3]], dtype=int32)
    >>> _.shape
    (1, 3)

    Expand the trailing dimension:

    >>> jnp.expand_dims(x, 1)
    Array([[1],
           [2],
           [3]], dtype=int32)
    >>> _.shape
    (3, 1)

    Expand multiple dimensions:

    >>> jnp.expand_dims(x, (0, 1, 3))
    Array([[[[1],
             [2],
             [3]]]], dtype=int32)
    >>> _.shape
    (1, 1, 3, 1)

    Dimensions can also be expanded more succinctly by indexing with ``None``:

    >>> x[None]  # equivalent to jnp.expand_dims(x, 0)
    Array([[1, 2, 3]], dtype=int32)
    >>> x[:, None]  # equivalent to jnp.expand_dims(x, 1)
    Array([[1],
           [2],
           [3]], dtype=int32)
    >>> x[None, None, :, None]  # equivalent to jnp.expand_dims(x, (0, 1, 3))
    Array([[[[1],
             [2],
             [3]]]], dtype=int32)
  """
  a = util.ensure_arraylike("expand_dims", a)
  axis = _ensure_index_tuple(axis)
  return lax.expand_dims(a, axis)


def expand_dims(x: Array['*d'], *, axis) -> Array['*d']:
  """`xnp.expand_dims(x, axis=axis)`."""
  xnp = lazy.get_xnp(x)
  if lazy.is_torch(x):
    return xnp.unsqueeze(x, axis=axis)
  else:
    return xnp.expand_dims(x, axis=axis)

