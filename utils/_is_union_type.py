from typing import Union

def _is_union_type(type_spec: type) -> bool:  # pylint: disable=g-bare-generic drop when 3.7 support is not needed
  """Cheeck if a type_spec is a Union type or not."""
  # UnionType was only introduced in python 3.10. We need getattr for
  # backward compatibility.
  return get_origin(type_spec) in [Union, getattr(types, 'UnionType', Union)]

