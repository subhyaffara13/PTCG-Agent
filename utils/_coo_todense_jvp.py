
def _coo_todense_jvp(data_dot, data, row, col, *, spinfo):
  return _coo_todense(data_dot, row, col, spinfo=spinfo)

