
def _select_dtype_rule(which, *cases):
  check_same_dtypes("select", *cases)
  if (not dtypes.issubdtype(which.dtype, np.bool_) and
      not dtypes.issubdtype(which.dtype, np.integer)):
    raise TypeError("select `which` must be boolean or integer type, got "
                    f"{which.dtype}.")
  if dtypes.issubdtype(which.dtype, np.bool_) and len(cases) > 2:
    raise TypeError("select with boolean `which` cannot have > 2 cases.")
  return cases[0].dtype

