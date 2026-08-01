
def _safe_cast(value, field_type, type_safe=False):
  """Helper function to handle the exceptional type conversions.

  This function implements the following exceptions for type-checking rules:

  * An `int` will be converted to a `float` if overriding a `float` field.
  * Any string value can override a `str` or `unicode` field. The value is
  converted to `field_type`.
  * A `tuple` will be converted to a `list` if overriding a `list` field.
  * A `list` will be converted to a `tuple` if overriding `tuple` field.
  * Short and long integers are indistinguishable. The final value will always
  be a `long` if both types are present.

  Args:
    value: The value to be assigned.
    field_type: The type for the field that we would like to assign value to.
    type_safe: If True, the method will throw an error if the `value` is not of
        type `field_type` after safe type conversions.

  Returns:
    The converted type-safe version of the value if it is one of the cases
    described. Otherwise, return the value without conversion.

  Raises:
    TypeError: if types don't match  after safe type conversions.
  """
  original_value_type = type(value)

  # The int->float exception.
  if isinstance(value, int) and field_type is float:
    return float(value)

  # The unicode/string to string exception.
  if isinstance(value, str) and field_type is str:
    return field_type(value)

  # tuple<->list conversion. JSON serialization converts lists to tuples, so
  # we need this to avoid errors when overriding a list field with its
  # deserialized version. See b/34805906 for more details.
  if isinstance(value, tuple) and field_type is list:
    return list(value)
  if isinstance(value, list) and field_type is tuple:
    return tuple(value)

  if isinstance(value, int) and field_type is int:
    return value

  if type_safe and _is_type_safety_violation(value, field_type):
    raise TypeError(
        '{} is of original type {} and cannot be casted to type {}'
        .format(value, str(original_value_type), str(field_type)))
  return value

