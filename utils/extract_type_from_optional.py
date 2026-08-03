from typing import Optional

def extract_type_from_optional(type_spec: type) -> Optional[type]:  # pylint: disable=g-bare-generic drop when 3.7 support is not needed
  """If type_spec is of type Optional[T], returns T object, otherwise None"""
  if not _is_union_type(type_spec):
    return None
  non_none = [t for t in get_args(type_spec) if t is not NoneType]
  if len(non_none) != 1:
    return None
  return non_none[0]

