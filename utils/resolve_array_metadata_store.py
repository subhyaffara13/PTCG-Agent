import logging

def resolve_array_metadata_store(
    type_handler_registry: types.TypeHandlerRegistry,
) -> Store | None:
  """Returns the ArrayMetadata Store or None.

  Gets ArrayMetadata Store from TypeHandler for jax.Array. ArrayMetadata
  persistence is only supported for jax.Array.

  Args:
    type_handler_registry: TypeHandlerRegistry to search TypeHandler for
      jax.Array.
  """
  try:
    array_handler = type_handler_registry.get(jax.Array)
  except ValueError:
    logging.warning(
        'No jax.Array in TypeHandlerRegistry: ArrayMetadata persistence is'
        ' disabled.'
    )
    return None
  else:
    if hasattr(array_handler, '_array_metadata_store'):
      return array_handler._array_metadata_store  # pylint: disable=protected-access
    else:
      logging.warning(
          'No ArrayMetadata Store defined in TypeHandler for jax.Array: %s!'
          ' Subchunking is disabled.',
          array_handler.__class__.__qualname__,
      )
      return None

