
def _is_type_safety_violation(value, field_type):
  """Helper function for type safety exceptions.

  This function determines whether or not assigning a value to a field violates
  type safety.

  Args:
    value: The value to be assigned.
    field_type: Type of the field that we would like to assign value to.

  Returns:
    True if assigning value to field violates type safety, False otherwise.
  """
  # Allow None to override and be overridden by any type.
  if value is None or field_type == _NoneType:
    return False
  elif isinstance(value, field_type):
    return False
  else:
    # A callable can overridde a callable.
    return not (callable(value) and _is_callable_type(field_type))

