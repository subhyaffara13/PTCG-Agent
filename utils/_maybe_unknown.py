from typing import Any

def _maybe_unknown(x: Any) -> pe.PartialVal:
  if isinstance(x, jax.ShapeDtypeStruct):
    return pe.PartialVal.unknown(core.ShapedArray(x.shape, x.dtype))
  else:
    return pe.PartialVal.known(x)

