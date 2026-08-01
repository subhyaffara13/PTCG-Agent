
def _as_shaped_array(t: jax.ShapeDtypeStruct) -> jax_core.ShapedArray:
  return jax_core.ShapedArray(t.shape, np.dtype(t.dtype))

