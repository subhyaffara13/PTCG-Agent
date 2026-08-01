
def _index_to_gather(indexer: NDIndexer, *, x_sharding: NamedSharding | Any,
                     normalize_indices: bool = True) -> _GatherIndexer:
  indexer.validate_slices()
  indexer = indexer.convert_sequences_to_arrays()

  is_advanced = np.nonzero(
    np.array([idx.typ in {IndexType.ARRAY, IndexType.INTEGER} for idx in indexer.indices]))
  advanced_axes_are_contiguous = np.all(np.diff(is_advanced) == 1)

  indexer = indexer.expand_ellipses()

  scalar_bool_dims: Sequence[int] = [n for n, i in enumerate(indexer.indices) if i.typ == IndexType.BOOLEAN]
  indexer, x_spec = indexer.expand_scalar_bool_indices(x_sharding.spec)

  if normalize_indices:
    indexer = indexer.normalize_indices()

  # Check for advanced indexing:
  # https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#advanced-indexing

  # The advanced indices.
  advanced_indexes: Sequence[Array] = []

  # The positions of the advanced indexing axes in `idx`.
  idx_advanced_axes: Sequence[int] = []

  # The positions of the advanced indexes in x's shape.
  # collapsed, after None axes have been removed. See below.
  x_advanced_axes: Sequence[int] = []

  if indexer.is_advanced_int_indexer():
    idx_without_none = [(i, d) for i, d in enumerate(indexer.indices) if d.typ != IndexType.NONE]
    advanced_pairs = (
      (lax_numpy.asarray(e.index), i, j)
      for j, (i, e) in enumerate(idx_without_none)
      if e.typ in [IndexType.ARRAY, IndexType.INTEGER]
    )
    advanced_indexes, idx_advanced_axes, x_advanced_axes = unzip3(advanced_pairs)

  x_axis = 0  # Current axis in x.
  y_axis = 0  # Current axis in y, before collapsing. See below.
  collapsed_y_axis = 0  # Current axis in y, after collapsing.

  # Scatter dimension numbers.
  offset_dims: list[int] = []
  collapsed_slice_dims: list[int] = []
  start_index_map: list[int] = []

  index_dtype = lax_utils.int_dtype_for_shape(indexer.shape, signed=True)

  # Gather indices.
  # Pairs of (array, start_dim) values. These will be broadcast into
  # gather_indices_shape, with the array dimensions aligned to start_dim, and
  # then concatenated.
  gather_indices: list[tuple[Array, int]] = []
  gather_indices_shape: list[int] = []

  # We perform three transformations to y before the scatter op, in order:
  # First, y is broadcast to slice_shape. In general `y` only need broadcast to
  # the right shape.
  slice_shape: list[int] = []
  # Next, y is squeezed to remove newaxis_dims. This removes np.newaxis/`None`
  # indices, which the scatter cannot remove itself.
  newaxis_dims: list[int] = []
  # Finally, we reverse reversed_y_dims to handle slices with negative strides.
  reversed_y_dims: list[int] = []

  gather_slice_shape: list[int] = []
  slice_spec = []

  for idx_pos, index in enumerate(indexer.indices):
    # Handle the advanced indices here if:
    # * the advanced indices were not contiguous and we are the start.
    # * we are at the position of the first advanced index.
    if (advanced_indexes and
        (advanced_axes_are_contiguous and idx_pos == idx_advanced_axes[0] or
         not advanced_axes_are_contiguous and idx_pos == 0)):
      advanced_index_arrs = util._broadcast_arrays(*advanced_indexes)
      shape = advanced_index_arrs[0].shape
      aia_spec = core.typeof(advanced_index_arrs[0]).sharding.spec
      ndim = len(shape)

      start_dim = len(gather_indices_shape)
      gather_indices.extend(
          (lax.convert_element_type(a, index_dtype), start_dim)
          for a in advanced_index_arrs
      )
      gather_indices_shape += shape

      assert x_advanced_axes is not None
      start_index_map.extend(x_advanced_axes)
      collapsed_slice_dims.extend(x_advanced_axes)
      slice_shape.extend(shape)
      slice_spec.extend(aia_spec)
      y_axis += ndim
      collapsed_y_axis += ndim

    # Per-index bookkeeping for advanced indexes.
    if idx_pos in idx_advanced_axes:
      x_axis += 1
      gather_slice_shape.append(1)
      continue

    if index.typ in [IndexType.INTEGER, IndexType.ARRAY] and np.ndim(index.index) == 0:  # pyrefly: ignore[bad-argument-type]
      # Basic scalar int indices
      if core.definitely_equal(indexer.shape[x_axis], 0):
        # XLA gives error when indexing into an axis of size 0
        raise IndexError(f"index is out of bounds for axis {x_axis} with size 0")
      i_converted = lax.convert_element_type(index.index, index_dtype)  # pyrefly: ignore[bad-argument-type]
      gather_indices.append((i_converted, len(gather_indices_shape)))
      collapsed_slice_dims.append(x_axis)
      gather_slice_shape.append(1)
      start_index_map.append(x_axis)
      x_axis += 1

    elif index.typ == IndexType.NONE:
      # None indexing: add a dimension.
      slice_shape.append(1)
      slice_spec.append(None)
      newaxis_dims.append(y_axis)
      y_axis += 1

    elif index.typ in [IndexType.SLICE, IndexType.DYNAMIC_SLICE]:
      # Handle static slice index.
      if isinstance(index.index, indexing.Slice):
        start, step, slice_size = index.index.start, index.index.stride, index.index.size
      elif isinstance(index.index, slice):
        start, step, slice_size = core.canonicalize_slice(index.index, indexer.shape[x_axis])
      else:
        raise RuntimeError(f"Internal: expected slice or Slice, got {type(index.index)}")
      slice_shape.append(slice_size)
      slice_spec.append(x_spec[x_axis])

      if core.definitely_equal(step, 1):
        # Optimization: avoid generating trivial gather.
        if not core.definitely_equal(slice_size, indexer.shape[x_axis]):
          gather_indices.append((lax.convert_element_type(start, index_dtype),
                                len(gather_indices_shape)))
          start_index_map.append(x_axis)
        gather_slice_shape.append(slice_size)
        offset_dims.append(collapsed_y_axis)
      else:
        indices = (lax_numpy.array(start, dtype=index_dtype) +
                   lax_numpy.array(step, dtype=index_dtype) * lax.iota(index_dtype, slice_size))
        if step < 0:
          reversed_y_dims.append(collapsed_y_axis)
          indices = lax.rev(indices, dimensions=(0,))

        gather_slice_shape.append(1)
        gather_indices.append((indices, len(gather_indices_shape)))
        start_index_map.append(x_axis)
        gather_indices_shape.append(slice_size)
        collapsed_slice_dims.append(x_axis)

      collapsed_y_axis += 1
      y_axis += 1
      x_axis += 1
    else:
      raise IndexError(f"Got unsupported indexer at position {idx_pos}: {index!r}")

  if len(gather_indices) == 0:
    gather_indices_array: ArrayLike = np.zeros((0,), dtype=index_dtype)
  elif len(gather_indices) == 1:
    g, _ = gather_indices[0]
    gather_indices_array = lax.expand_dims(g, (g.ndim,))
  else:
    last_dim = len(gather_indices_shape)
    gather_indices_shape.append(1)
    gather_indices_array = lax.concatenate([
      lax.broadcast_in_dim(g, gather_indices_shape, tuple(range(i, i + g.ndim)))
      for g, i in gather_indices],
      last_dim)

  dnums = slicing.GatherDimensionNumbers(
    offset_dims = tuple(offset_dims),
    collapsed_slice_dims = tuple(sorted(collapsed_slice_dims)),
    start_index_map = tuple(start_index_map)
  )
  slice_sharding = canonicalize_sharding(x_sharding.update(spec=slice_spec),
                                         "index_to_gather")
  return _GatherIndexer(
    slice_shape=slice_shape,
    newaxis_dims=tuple(newaxis_dims),
    gather_slice_shape=gather_slice_shape,
    reversed_y_dims=reversed_y_dims,
    dnums=dnums,
    gather_indices=gather_indices_array,
    unique_indices=not advanced_indexes,
    indices_are_sorted=not advanced_indexes,
    scalar_bool_dims=scalar_bool_dims,
    slice_sharding=slice_sharding)

