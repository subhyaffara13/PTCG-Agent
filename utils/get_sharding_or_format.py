
def get_sharding_or_format(
    value: Any, *, support_format: bool = False
) -> jax.sharding.Sharding | Format | None:  # pytype: disable=unsupported-operands
  """Returns the Format if it exists, then the Sharding if it exists, otherwise None."""

  if hasattr(value, 'sharding'):
    if (
        support_format
        and hasattr(value, 'format')
        and get_device_local_layout(value)
    ):
      # value is a jax.Array or a jax.ShapeDtypeStruct.
      return value.format
    else:
      return value.sharding
  else:
    return None

