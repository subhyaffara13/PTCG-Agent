
def _coo_matmat_jvp_right(B_dot, data, row, col, B, *, spinfo, transpose):
  return _coo_matmat(data, row, col, B_dot, spinfo=spinfo, transpose=transpose)

