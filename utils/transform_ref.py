
def transform_ref(
    ref: pallas_core.TransformedRef,
    transform: state_types.Transform
) -> pallas_core.TransformedRef:
  if not isinstance(ref, pallas_core.TransformedRef):
    if not isinstance(jax_core.typeof(ref), state_types.AbstractRef):
      raise TypeError("ref must be a reference")
    ref = pallas_core.TransformedRef(ref, transforms=())
  return pallas_core.TransformedRef(
      ref.ref, (*ref.transforms, transform),
  )

