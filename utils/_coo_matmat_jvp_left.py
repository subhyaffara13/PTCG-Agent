
def _coo_matmat_jvp_left(data_dot, data, row, col, B, *, spinfo, transpose):
  return _coo_matmat(data_dot, row, col, B, spinfo=spinfo, transpose=transpose)

