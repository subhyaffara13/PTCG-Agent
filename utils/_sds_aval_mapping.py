
def _sds_aval_mapping(x):
  aval = ShapedArray(
      x.shape, dtypes.canonicalize_dtype(x.dtype, allow_extended_dtype=True),
      weak_type=x.weak_type)
  aval = update_aval_with_sharding(aval, x.sharding, mat=x.manual_axis_type)
  if x.is_ref:
    from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
    return AbstractRef(aval)
  return aval

