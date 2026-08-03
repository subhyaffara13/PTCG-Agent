from typing import Any

def _is_abstract_subprotocol(
    type_a: type[Any], type_b: type[Any]
) -> bool:
  """Checks if 'type_a' is a subclass or sub-protocol of 'type_b'."""
  try:
    if typing_extensions.is_protocol(type_b):   # pytype: disable=not-supported-yet
      return protocol_utils.is_subclass_protocol(
          cls=type_a, protocol=type_b
      )
    return issubclass(type_a, type_b)
  except TypeError:
    return False

