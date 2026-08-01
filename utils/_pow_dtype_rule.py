
def _pow_dtype_rule(x, y):
  if (dtypes.issubdtype(x.dtype, np.inexact) and
      dtypes.issubdtype(y.dtype, np.integer)):
    return x.dtype
  if x.dtype == y.dtype:
    return x.dtype
  raise TypeError("the first argument to pow must have an inexact dtype (float "
                  "or complex), and the second argument must have an inexact or"
                  " integer dtype, and two inexact dtypes must match, but got "
                  f"{x.dtype} and {y.dtype} respectively.")

