
def _coo_matvec_jvp_mat(data_dot, data, row, col, v, *, spinfo, transpose):
  return _coo_matvec(data_dot, row, col, v, spinfo=spinfo, transpose=transpose)

