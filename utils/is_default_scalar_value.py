import math


def IsDefaultScalarValue(value):
  """Returns whether or not a scalar value is the default value of its type.

  Specifically, this should be used to determine presence of implicit-presence
  fields, where we disallow custom defaults.

  Args:
    value: A scalar value to check.

  Returns:
    True if the value is equivalent to a default value, False otherwise.
  """
  if isinstance(value, numbers.Number) and math.copysign(1.0, value) < 0:
    # Special case for negative zero, where "truthiness" fails to give the right
    # answer.
    return False

  # Normally, we can just use Python's boolean conversion.
  return not value

