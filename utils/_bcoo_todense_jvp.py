
def _bcoo_todense_jvp(data_dot, data, indices, *, spinfo):
  return _bcoo_todense(data_dot, indices, spinfo=spinfo)

