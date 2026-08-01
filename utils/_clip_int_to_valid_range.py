
def _clip_int_to_valid_range(val: DimSize, dtype, where: str) -> int:
  info = np.iinfo(dtype)
  val = core.concrete_dim_or_error(val, where)
  return core.max_dim(info.min, core.min_dim(val, info.max))

