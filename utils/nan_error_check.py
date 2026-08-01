
def nan_error_check(prim, error, enabled_errors, *in_vals, **params):
  out = prim.bind(*in_vals, **params)
  err = check_nans(prim, error, enabled_errors, out)
  return err, out

