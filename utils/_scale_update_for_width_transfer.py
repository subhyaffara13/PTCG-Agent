
def _scale_update_for_width_transfer(
    update: jax.Array, dim_nums: MuonDimensionNumbers
):
  """Apply width scaling from <https://github.com/KellerJordan/Muon>."""
  fan_in, fan_out = _get_shape_products(update, dim_nums)
  scale = jnp.sqrt(jnp.maximum(1, fan_out / fan_in))
  return scale * update

