
def _set_error_if_nan(pred: Array, /):
  """Set the internal error state if any element of `pred` is `NaN`.

  This function is disabled if the `jax_error_checking_behavior_nan` flag is
  set to "ignore".
  """
  if config.error_checking_behavior_nan.value == "ignore":
    return

  if not dtypes.issubdtype(pred.dtype, np.floating):  # only check floats
    return

  error_check_lib.set_error_if(ufuncs.isnan(pred), "NaN encountered")

