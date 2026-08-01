
def _should_skip_type_check(old_value, new_value) -> bool:
  """Returns True if the type check should be skipped."""

  if not isinstance(new_value, FieldReference):
    return False
  # Skip type checking if value is a FieldReference of the same type, or
  # FieldReference is generic type.
  if new_value.get_type() in (type(old_value), object):
    return True
  else:
    return False

