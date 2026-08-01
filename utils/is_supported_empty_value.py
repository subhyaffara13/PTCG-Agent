
def is_supported_empty_value(
    value: Any,
    pytree_metadata_options: PyTreeMetadataOptions = (
        pytree_metadata_options_lib.PYTREE_METADATA_OPTIONS
    ),
) -> bool:
  """Determines if the *empty* `value` is supported without custom TypeHandler."""
  # Check isinstance first to avoid `not` checks on jax.Arrays (raises error).
  if tree_utils.isinstance_of_namedtuple(value):
    if pytree_metadata_options.support_rich_types and not value:
      return True
    return False
  return is_empty_container(value) or value is None

