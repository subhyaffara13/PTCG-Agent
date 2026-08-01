
def get_hlo_sharding_string(
    sharding: jax.sharding.Sharding,
    num_dimensions: int,
) -> str:
  """Serializes the sharding to an hlo-sharding, encodes it to base64 and returns the base-64 as an utf-8 string."""
  return base64_utf8_stringify(
      # pylint:disable=protected-access
      sharding._to_xla_hlo_sharding(num_dimensions)  # pytype: disable=attribute-error
      # pylint:enable=protected-access
      .to_proto().SerializeToString()
  )

