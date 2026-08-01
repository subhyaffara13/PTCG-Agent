
def compute_scale(amax, scale, fp8_max, margin=0):
  # The algorithm for computing the new scale is sourced from
  #   https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/api/jax.html#transformer_engine.jax.update_fp8_metas
  # wherein the `original_scale` corresponds to the reciprocal of the `scale`
  # passed in this function.
  scale = 1.0 / scale

  sf = (fp8_max / amax) / (2**margin)
  sf = jnp.where(amax > 0.0, sf, scale)
  sf = jnp.where(jnp.isfinite(amax), sf, scale)

  return 1.0 / sf

