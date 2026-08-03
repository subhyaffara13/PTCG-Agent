from typing import Callable

def _segment_update(name: str,
                    data: ArrayLike,
                    segment_ids: ArrayLike,
                    scatter_op: Callable,
                    num_segments: int | None = None,
                    indices_are_sorted: bool = False,
                    unique_indices: bool = False,
                    bucket_size: int | None = None,
                    reducer: Callable | None = None,
                    mode: slicing.GatherScatterMode | str | None = None,
                    out_sharding: NamedSharding | None = None) -> Array:
  check_arraylike(name, data, segment_ids)
  mode = slicing.GatherScatterMode.FILL_OR_DROP if mode is None else mode
  data = jnp.asarray(data)
  segment_ids = jnp.asarray(segment_ids)
  dtype = data.dtype
  if num_segments is None:
    num_segments = np.max(segment_ids) + 1
  num_segments = core.concrete_dim_or_error(num_segments, "segment_sum() `num_segments` argument.")
  if num_segments is not None and num_segments < 0:
    raise ValueError("num_segments must be non-negative.")

  if bucket_size is None:
    out = jnp.full((num_segments,) + data.shape[1:],
                   _get_identity(scatter_op, dtype), dtype=dtype)
    return _scatter_update(
      out, segment_ids, data, scatter_op, indices_are_sorted,
      unique_indices, normalize_indices=False, mode=mode,
      out_sharding=out_sharding)

  # Bucketize indices and perform segment_update on each bucket to improve
  # numerical stability for operations like product and sum.
  assert reducer is not None
  if out_sharding is not None:
    raise NotImplementedError
  num_buckets = util.ceil_of_ratio(segment_ids.size, bucket_size)
  out = jnp.full((num_buckets, num_segments) + data.shape[1:],
                 _get_identity(scatter_op, dtype), dtype=dtype)
  out = _scatter_update(
    out, np.index_exp[jnp.arange(segment_ids.shape[0]) // bucket_size,
                      segment_ids[None, :]],
    data, scatter_op, indices_are_sorted,
    unique_indices, normalize_indices=False, mode=mode)
  return reducer(out, axis=0).astype(dtype)

