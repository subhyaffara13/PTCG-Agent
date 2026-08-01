
def _scale_update_for_consistent_rms(
    update: jax.Array,
    dim_nums: MuonDimensionNumbers,
    consistent_rms: jax.typing.ArrayLike
):
  """Apply consistent RMS scaling from <https://arxiv.org/abs/2502.16982>."""
  fan_in, fan_out = _get_shape_products(update, dim_nums)
  scale = jnp.sqrt(jnp.maximum(fan_in, fan_out)) * consistent_rms
  return scale * update

