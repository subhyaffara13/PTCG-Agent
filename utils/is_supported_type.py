
def is_supported_type(
    value: Any,
    pytree_metadata_options: PyTreeMetadataOptions = (
        pytree_metadata_options_lib.PYTREE_METADATA_OPTIONS
    ),
) -> bool:
  """Determines if the `value` is supported without custom TypeHandler."""
  return isinstance(
      value,
      (str, int, float, np.number, np.ndarray, bytes, jax.Array),
  ) or empty_values.is_supported_empty_value(value, pytree_metadata_options)

