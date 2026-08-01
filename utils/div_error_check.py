
def div_error_check(error, enabled_errors, x, y):
  """Checks for division by zero and NaN."""
  if DivisionByZeroError in enabled_errors:
    any_zero = jnp.any(jnp.equal(y, 0))
    error = assert_func(error, any_zero, DivisionByZeroError(get_traceback()))
  return nan_error_check(lax.div_p, error, enabled_errors, x, y)

