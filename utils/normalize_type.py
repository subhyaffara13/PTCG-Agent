
def normalize_type(type: AnyStr | None, encode: bool | None = True) -> str | None:
    if not type:
        return None

    type_str = type if isinstance(type, str) else type.decode("utf-8")
    quoter = get_quoter(encode)
    type_str = quoter(type_str)
    return type_str.strip().lower() or None


def normalize_type(type_spec: type) -> type:  # pylint: disable=g-bare-generic drop when 3.7 support is not needed
  """Normalizes a type object.

  Strips all None types from the type specification and returns the remaining
  single type. This is primarily useful for Optional type annotations in which
  case it will strip out the NoneType and return the inner type.

  Args:
    type_spec: The type to normalize.

  Raises:
    TypeError: If there is not exactly 1 non-None type in the union.
  Returns:
    The normalized type.
  """
  if _is_union_type(type_spec):
    subtype = extract_type_from_optional(type_spec)
    if subtype is None:
      raise TypeError(f'Unable to normalize ambiguous type: {type_spec}')
    return subtype

  return type_spec

