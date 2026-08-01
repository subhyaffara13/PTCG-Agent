
def _coo_matvec_jvp_vec(v_dot, data, row, col, v, *, spinfo, transpose):
  return _coo_matvec(data, row, col, v_dot, spinfo=spinfo, transpose=transpose)

