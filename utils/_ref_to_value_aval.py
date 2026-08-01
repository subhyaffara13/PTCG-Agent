
def _ref_to_value_aval(ref):
  """Return the inner of a ref, or a ShapedArray for TransformedRefs."""
  return (
      jax_core.ShapedArray(shape=ref.shape, dtype=ref.dtype)
      if isinstance(ref, state.TransformedRef)
      else jax.typeof(ref).inner_aval
  )

