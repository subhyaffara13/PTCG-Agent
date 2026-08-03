from typing import Any

def spvalues_to_avals(
    spenv: SparsifyEnv,
    spvalues: Any,
    ) -> Any:
  """Convert a pytree of spvalues to an equivalent pytree of abstract values."""
  def spvalue_to_aval(spvalue):
    data = spenv.data(spvalue)
    return core.ShapedArray(spvalue.shape, data.dtype, data.aval.weak_type)
  return tree_map(spvalue_to_aval, spvalues, is_leaf=_is_spvalue)

