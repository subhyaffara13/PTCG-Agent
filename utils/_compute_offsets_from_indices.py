
def _compute_offsets_from_indices(
    block_info: BlockInfo, nd_indexer: NDIndexer
) -> ir.Value:
  full_shape = block_info.full_shape_dtype.shape
  num_squeezed_dims = sum(isinstance(b, pallas_core.Squeezed)
                          for b in block_info.block_shape)
  strides = pallas_utils.strides_from_shape(full_shape)
  indexer_shape = nd_indexer.get_indexer_shape_static()
  int_indexer_shape = nd_indexer.int_indexer_shape
  _check_tensor_size(indexer_shape)
  indices = nd_indexer.indices
  other_shape = indexer_shape[len(int_indexer_shape) :]
  other_shape_idx = 0
  assert len(indices) + num_squeezed_dims == len(full_shape)
  assert len(block_info.start_indices) == len(full_shape)

  array_dtype = jnp.dtype(block_info.full_shape_dtype.dtype)
  full_size = math.prod(full_shape) * array_dtype.itemsize
  # Use 64-bit indexing when offset might be >= 2**32 bytes.
  offset_eltype = ir.IntegerType.get_signless(64 if full_size > 2**32 else 32)
  if indexer_shape:
    offsets = _zeros(ir.RankedTensorType.get(indexer_shape, offset_eltype))
  else:
    offsets = _ir_constant(0, offset_eltype)

  indexer_iter = iter(indices)
  for dim_stride, dim_block_size, start_offset in zip(
      strides, block_info.block_shape, block_info.start_indices
  ):
    match dim_block_size:
      case pallas_core.Squeezed():
        index = _ir_constant(0, offset_eltype)
      case int():
        index = next(indexer_iter)
      case _:
        raise ValueError(f"Unexpected dim_block_size: {dim_block_size}")

    if isinstance(index, slice):
      index = primitives.Slice.from_slice(
          index, pallas_core.get_block_size(dim_block_size)
      )

    if isinstance(index, primitives.Slice):
      if index.is_dynamic_start or (index.stride != 1):
        if not index.is_dynamic_start:
          start = _ir_constant(index.start, offset_eltype)
        else:
          assert isinstance(index.start, ir.Value)
          start = index.start
        start = _ir_cast(start, offset_eltype, signed=False)

        iota = _ir_cast(
            _make_range(0, int(index.size)), offset_eltype, signed=False
        )
        if index.stride != 1:
          iota = _mul(iota, _full(iota.type, index.stride))
        dim_offsets = _add(_bcast_to(start, (int(index.size),)), iota)
      else:
        iota = _make_range(int(index.start), int(index.start + index.size))
        dim_offsets = _ir_cast(iota, offset_eltype, signed=False)

      other_shape_idx += 1
      for _ in other_shape[other_shape_idx:]:
        rank = ir.RankedTensorType(dim_offsets.type).rank
        dim_offsets = _expand_dims(dim_offsets, rank)
    else:
      # indexer is either a *scalar* or an array of size `int_indexer_shape`
      dim_offsets = index
      if not isinstance(dim_offsets, ir.Value):
        dim_offsets = _ir_constant(dim_offsets, offset_eltype)
      dim_offsets = _ir_cast(dim_offsets, offset_eltype, signed=False)

      if isinstance(dim_offsets.type, ir.RankedTensorType):
        for _ in other_shape:
          rank = ir.RankedTensorType(dim_offsets.type).rank
          dim_offsets = _expand_dims(dim_offsets, rank)

    if isinstance(dim_offsets.type, ir.RankedTensorType):
      rank = ir.RankedTensorType(dim_offsets.type).rank
      for _ in range(len(indexer_shape) - rank):
        dim_offsets = _expand_dims(dim_offsets, 0)
    dim_offsets = _bcast_to(dim_offsets, indexer_shape)

    if start_offset is not None:
      start_offset = _ir_cast(start_offset, offset_eltype, signed=False)
      dim_offsets = _add(dim_offsets, _bcast_to(start_offset, indexer_shape))

    dim_offsets = _mul(dim_offsets, _full(dim_offsets.type, dim_stride))
    offsets = _add(offsets, dim_offsets)

  return offsets

