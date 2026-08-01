
def _check_consumed_value(eqn, consumed):
  """Extra check for use with assert_consumed_value_p"""
  expected = eqn.params['value'].val
  if not np.all(consumed == expected):
    if np.all(expected):
      raise AssertionError(f"Expected key to be consumed in {eqn}")
    elif not np.any(expected):
      raise AssertionError(f"Expected key to not be consumed in {eqn}")
    else:
      raise AssertionError(f"Expected {expected}, got {consumed} in {eqn}")

