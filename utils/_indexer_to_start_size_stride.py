from typing import Any

def _indexer_to_start_size_stride(
    indexer: NDIndexer,
    ref_block_shape: tuple[int | pallas_core.Squeezed, ...],
    *,
    cast_to_index: bool,
) -> tuple[
    tuple[ir.Value, ...],
    tuple[int | ir.Value, ...],
    tuple[int, ...],
    tuple[bool, ...],
    tuple[int | pallas_core.Squeezed, ...],
]:
  indices_iter = iter(indexer.indices)
  starts, sizes, strides, squeeze_dims = [], [], [], []
  for s in ref_block_shape:
    match s:
      case pallas_core.Squeezed():
        start = _maybe_cast_to_index(cast_to_index, 0)
        size = 1
        stride = 1
        squeeze_dim = True
      case _:
        idx = cast(Any, next(indices_iter))
        start, size, stride, squeeze_dim = _index_to_start_size_stride(
            idx, cast_to_index
        )
    starts.append(start)
    sizes.append(size)
    strides.append(stride)
    squeeze_dims.append(squeeze_dim)
  next_index = next(indices_iter, None)
  assert next_index is None, (indexer.indices, ref_block_shape)
  new_ref_block_shape = tuple(s for s, squeeze in zip(sizes, squeeze_dims)
                              if not squeeze)
  return (
      tuple(starts),
      tuple(sizes),
      tuple(strides),
      tuple(squeeze_dims),
      new_ref_block_shape,
  )

