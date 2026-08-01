
def infer_tiling(
    ty: jax_core.AbstractValue, tiling: Tiling | None = None
) -> tuple[int | None, ...]:
  """Compute a tiling for the given shape and type.

  For an n-dimensional shape, returns the tiling for the last
  ``len(tiling.shape)`` dimensions and 1 for the leading dims. For example:
  - 2D tiling: (256, 256) -> (8, 128) and (2, 3, 128, 128) -> (1, 1, 8, 128).
  - 1D tiling: (16,) -> (8,) and (2, 3, 8) -> (1, 1, 8).

  Types are not required to have a dtype, so for such types we return None for
  all dimensions because their tiling is unknown.
  """
  assert hasattr(ty, "shape")
  shape = ty.shape
  if not hasattr(ty, "dtype"):
    return (None,) * len(shape)
  if ty.dtype == jnp.dtype("int4"):
    packing = 8
  else:
    packing = 4 // ty.dtype.itemsize

  if tiling is None:
    tiling = Tiling.COMPACT
  tiling_rank = len(tiling.shape)
  if len(shape) == 1 and tiling == Tiling.COMPACT:
    _, lane_count = tiling.shape
    tpu_generation = get_tpu_info().generation
    return ((1 + int(tpu_generation < 4)) * packing * lane_count,)
  if len(shape) < tiling_rank:
    raise ValueError(
        f"Shape must have at least {tiling_rank} dimensions: {shape=}"
    )

  leading_dims, final_dims = shape[:-tiling_rank], shape[-tiling_rank:]
  match tiling:
    case Tiling.COMPACT:
      second_minor, _ = final_dims
      factor = _get_tiling_factor(second_minor, tiling.shape[0], packing)
      return (*(1,) * len(leading_dims), factor, tiling.shape[1])
    case Tiling.SPARSE_CORE:
      [tile_size] = tiling.shape
      return (*(1,) * len(leading_dims), tile_size * packing)

