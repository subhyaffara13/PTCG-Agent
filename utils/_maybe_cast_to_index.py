
def _maybe_cast_to_index(cast_to_index, x):
  if cast_to_index:
    return _make_index(x)
  return _ensure_mlir_value(x, aval=pallas_core.index_map_grid_aval)

