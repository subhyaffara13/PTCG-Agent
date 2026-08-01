
def _maybe_physicalize_block_shape(aval, block_shape):
  if should_physicalize_dtype(aval.dtype):
    physical_element_aval = jax_core.physical_element_aval(aval.dtype)
    block_shape += physical_element_aval.shape
  return block_shape

