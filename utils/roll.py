
def roll(a: ArrayLike, shift, axis=None):
    if axis is not None:
        axis = _util.normalize_axis_tuple(axis, a.ndim, allow_duplicate=True)
        if not isinstance(shift, tuple):
            shift = (shift,) * len(axis)
    return torch.roll(a, shift, axis)


def roll(a: TensorLikeType, shifts: DimsType, dims: DimsType = ()) -> TensorLikeType:
    """Reference implementation of :func:`torch.roll`."""

    dims = utils.canonicalize_dims(a.ndim, dims)
    # ATen specifies int[1] type for shifts and dims which expands integers to tuples of length 1
    if not isinstance(shifts, Iterable):
        shifts = (shifts,)
    if not isinstance(dims, Iterable):
        dims = (dims,)

    # Avoid modulo by zero
    if a.numel() == 0:
        # Keeping this as ref for now as FakeTensor runs into some issues with complex tensors
        return a.clone()

    # pyrefly: ignore [bad-argument-type]
    if a.dim() == 0 and len(dims) > 0:
        raise IndexError(
            # pyrefly: ignore [bad-index, index-error]
            f"Dimension specified as {dims[0]} but tensor has no dimensions"
        )

    # pyrefly: ignore [bad-argument-type]
    len_shifts = len(shifts)
    # pyrefly: ignore [bad-argument-type]
    len_dims = len(dims)
    if len_shifts != 1 or len_dims != 1:
        if len_shifts == 0:
            raise RuntimeError("`shifts` required")
        # Takes care of the case when dims is not specified (default)
        # By default, the tensor is flattened before shifting, after which the original shape is restored
        if len_dims == 0 and len_shifts == 1:
            return torch.roll(torch.flatten(a), shifts, 0).view(a.shape)
        if len_shifts != len_dims:
            raise RuntimeError(
                f"shifts and dimensions must align. shifts: {len_shifts}, dims: {len_dims}"
            )
        if len_dims <= 1:
            raise AssertionError(f"Expected len_dims > 1, got {len_dims}")
        # pyrefly: ignore [bad-index]
        tail_shifts = shifts[1:]
        # pyrefly: ignore [bad-index, index-error]
        tail_dims = dims[1:]
        # pyrefly: ignore [bad-index, index-error]
        # pyrefly: ignore [bad-index, index-error]
        first_dim_rolled = torch.roll(a, (shifts[0],), dims[0])
        return torch.roll(first_dim_rolled, tail_shifts, tail_dims)

    # This path is taken when only one dimension is rolled
    # For example to get `first_dim_rolled` above
    # pyrefly: ignore [bad-index, index-error]
    dim = dims[0]
    size = a.shape[dim]
    # pyrefly: ignore [bad-index, index-error]
    start = (size - shifts[0]) % size
    idx = torch.arange(size, device=a.device)
    return a.index_select(dim, torch.fmod(start + idx, size))


def roll(g: jit_utils.GraphContext, self, shifts, dims):
    if len(shifts) != len(dims):
        raise AssertionError(f"len(shifts)={len(shifts)} != len(dims)={len(dims)}")

    result = self
    for i in range(len(shifts)):
        shapes = []
        shape = symbolic_helper._slice_helper(
            g, result, axes=[dims[i]], starts=[-shifts[i]], ends=[sys.maxsize]
        )
        shapes.append(shape)
        shape = symbolic_helper._slice_helper(
            g, result, axes=[dims[i]], starts=[0], ends=[-shifts[i]]
        )
        shapes.append(shape)
        result = g.op("Concat", *shapes, axis_i=dims[i])

    return result


def roll(x: Array, /, shift: int | tuple[int, ...], *, axis: int | tuple[int, ...] | None = None, **kwargs: object) -> Array:
    return torch.roll(x, shift, axis, **kwargs)


def roll(a, shift, axis=None):
    """
    Roll array elements along a given axis.

    Elements that roll beyond the last position are re-introduced at
    the first.

    Parameters
    ----------
    a : array_like
        Input array.
    shift : int or tuple of ints
        The number of places by which elements are shifted.  If a tuple,
        then `axis` must be a tuple of the same size, and each of the
        given axes is shifted by the corresponding number.  If an int
        while `axis` is a tuple of ints, then the same value is used for
        all given axes.
    axis : int or tuple of ints, optional
        Axis or axes along which elements are shifted.  By default, the
        array is flattened before shifting, after which the original
        shape is restored.

    Returns
    -------
    res : ndarray
        Output array, with the same shape as `a`.

    See Also
    --------
    rollaxis : Roll the specified axis backwards, until it lies in a
               given position.

    Notes
    -----
    Supports rolling over multiple dimensions simultaneously.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(10)
    >>> np.roll(x, 2)
    array([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])
    >>> np.roll(x, -2)
    array([2, 3, 4, 5, 6, 7, 8, 9, 0, 1])

    >>> x2 = np.reshape(x, (2, 5))
    >>> x2
    array([[0, 1, 2, 3, 4],
           [5, 6, 7, 8, 9]])
    >>> np.roll(x2, 1)
    array([[9, 0, 1, 2, 3],
           [4, 5, 6, 7, 8]])
    >>> np.roll(x2, -1)
    array([[1, 2, 3, 4, 5],
           [6, 7, 8, 9, 0]])
    >>> np.roll(x2, 1, axis=0)
    array([[5, 6, 7, 8, 9],
           [0, 1, 2, 3, 4]])
    >>> np.roll(x2, -1, axis=0)
    array([[5, 6, 7, 8, 9],
           [0, 1, 2, 3, 4]])
    >>> np.roll(x2, 1, axis=1)
    array([[4, 0, 1, 2, 3],
           [9, 5, 6, 7, 8]])
    >>> np.roll(x2, -1, axis=1)
    array([[1, 2, 3, 4, 0],
           [6, 7, 8, 9, 5]])
    >>> np.roll(x2, (1, 1), axis=(1, 0))
    array([[9, 5, 6, 7, 8],
           [4, 0, 1, 2, 3]])
    >>> np.roll(x2, (2, 1), axis=(1, 0))
    array([[8, 9, 5, 6, 7],
           [3, 4, 0, 1, 2]])

    """
    a = asanyarray(a)
    if axis is None:
        return roll(a.ravel(), shift, 0).reshape(a.shape)

    else:
        axis = normalize_axis_tuple(axis, a.ndim, allow_duplicate=True)
        broadcasted = broadcast(shift, axis)
        if broadcasted.ndim > 1:
            raise ValueError(
                "'shift' and 'axis' should be scalars or 1D sequences")
        shifts = dict.fromkeys(range(a.ndim), 0)
        for sh, ax in broadcasted:
            shifts[ax] += int(sh)

        rolls = [((slice(None), slice(None)),)] * a.ndim
        for ax, offset in shifts.items():
            offset %= a.shape[ax] or 1  # If `a` is empty, nothing matters.
            if offset:
                # (original, result), (original, result)
                rolls[ax] = ((slice(None, -offset), slice(offset, None)),
                             (slice(-offset, None), slice(None, offset)))

        result = empty_like(a)
        for indices in itertools.product(*rolls):
            arr_index, res_index = zip(*indices)
            result[res_index] = a[arr_index]

        return result


def roll(a: ArrayLike, shift: ArrayLike | Sequence[int],
         axis: int | Sequence[int] | None = None) -> Array:
  """Roll the elements of an array along a specified axis.

  JAX implementation of :func:`numpy.roll`.

  Args:
    a: input array.
    shift: the number of positions to shift the specified axis. If an integer,
      all axes are shifted by the same amount. If a tuple, the shift for each
      axis is specified individually.
    axis: the axis or axes to roll. If ``None``, the array is flattened, shifted,
      and then reshaped to its original shape.

  Returns:
    A copy of ``a`` with elements rolled along the specified axis or axes.

  See also:
    - :func:`jax.numpy.rollaxis`: roll the specified axis to a given position.

  Examples:
    >>> a = jnp.array([0, 1, 2, 3, 4, 5])
    >>> jnp.roll(a, 2)
    Array([4, 5, 0, 1, 2, 3], dtype=int32)

    Roll elements along a specific axis:

    >>> a = jnp.array([[ 0,  1,  2,  3],
    ...                [ 4,  5,  6,  7],
    ...                [ 8,  9, 10, 11]])
    >>> jnp.roll(a, 1, axis=0)
    Array([[ 8,  9, 10, 11],
           [ 0,  1,  2,  3],
           [ 4,  5,  6,  7]], dtype=int32)
    >>> jnp.roll(a, [2, 3], axis=[0, 1])
    Array([[ 5,  6,  7,  4],
           [ 9, 10, 11,  8],
           [ 1,  2,  3,  0]], dtype=int32)
  """
  arr = util.ensure_arraylike("roll", a)
  if axis is None:
    return roll(arr.ravel(), shift, 0).reshape(arr.shape)
  axis = _ensure_index_tuple(axis)
  axis = tuple(_canonicalize_axis(ax, arr.ndim) for ax in axis)
  try:
    shift = _ensure_index_tuple(shift)
  except TypeError:
    return _roll_dynamic(arr, asarray(shift), axis)
  else:
    return _roll_static(arr, shift, axis)


def roll(
    x: jax.Array,
    shift: jax.Array | int,
    axis: int,
    *,
    stride: int | None = None,
    stride_axis: int | None = None,
) -> jax.Array:
  if isinstance(shift, int) and shift < 0:
    raise ValueError("shift must be non-negative.")
  if axis < 0 or axis >= len(x.shape):
    raise ValueError("axis is out of range.")
  if (stride is None) != (stride_axis is None):
    raise ValueError("stride and stride_axis must be both specified or not.")
  if stride is not None and stride_axis is not None:
    if stride < 0:
      raise ValueError("stride must be non-negative.")
    if stride_axis < 0 or stride_axis >= len(x.shape):
      raise ValueError("stride_axis is out of range")
    if axis == stride_axis:
      raise ValueError("expected axis and stride_axis are different.")
  return roll_p.bind(
      x, shift, axis=axis, stride=stride, stride_axis=stride_axis
  )

