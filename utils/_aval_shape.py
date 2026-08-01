
def _aval_shape(aval: core.AbstractValue) -> Shape:
  if isinstance(aval, core.AbstractFuture):
    # An AbstractFuture is a future of an array. While the array has a shape,
    # the future itself acts more like a token, which has no shape.
    return ()
  return () if aval is core.abstract_token else core.physical_aval(aval).shape  # pyrefly: ignore[missing-attribute]

