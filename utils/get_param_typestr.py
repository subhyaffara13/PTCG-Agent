from typing import Any

def get_param_typestr(
    value: Any,
    registry: types.TypeHandlerRegistry,
    pytree_metadata_options: pytree_metadata_options_lib.PyTreeMetadataOptions,
) -> str:
  """Retrieves the typestr for a given value."""
  if empty_values.is_supported_empty_value(value, pytree_metadata_options):
    typestr = empty_values.get_empty_value_typestr(
        value, pytree_metadata_options
    )
  else:
    try:
      handler = registry.get(type(value))
      typestr = handler.typestr()
    except ValueError:
      # Not an error because users' training states often have a bunch of
      # random unserializable objects in them (empty states, optimizer
      # objects, etc.). An error occurring due to a missing TypeHandler
      # will be surfaced elsewhere.
      typestr = empty_values.RESTORE_TYPE_NONE
  return typestr

