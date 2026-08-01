
def aval_qdd_from_current_val(aval, x):
  if aval.has_qdd:
    return cur_aval_qdd(x)
  else:
    return aval

