
def apply_unswizzle_and_untile(
    transforms: tuple[state_types.Transform, ...],
    aval: jax_core.AbstractValue,
) -> jax_core.AbstractValue:
  if not all(isinstance(t, (mosaic_gpu_core.UnswizzleRef,
                            mosaic_gpu_core.UntilingTransform))
             for t in transforms):
    raise ValueError("Unsupported transforms:", transforms)
  return state_types.TransformedRef(aval, transforms).type

