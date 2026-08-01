
def _set_error_if_divide_by_zero(pred: Array, /):
  """Set the internal error state if any element of `pred` is zero.

  This function is intended for checking if the denominator of a division is
  zero.

  This function is disabled if the `jax_error_checking_behavior_divide` flag is
  set to "ignore".
  """
  if config.error_checking_behavior_divide.value == "ignore":
    return

  zero = array_creation.zeros_like(pred, shape=())
  error_check_lib.set_error_if(pred == zero, "Division by zero encountered")

