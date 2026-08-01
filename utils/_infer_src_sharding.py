
def _infer_src_sharding(src, x, x_aval) -> Sharding | None:
  if src is not None:
    return src
  if isinstance(x, array.ArrayImpl):
    return x.sharding
  if isinstance(x, core.Tracer):
    val = x.to_concrete_value()
    if val is not None and isinstance(val, array.ArrayImpl):
      return val.sharding
  if x_aval is not core.abstract_token and x_aval.sharding.mesh.are_all_axes_explicit:
    return x_aval.sharding.update(
        memory_kind=core.mem_space_to_kind(x_aval.memory_space))
  return None

