
def _bit_width(d):
  if dtypes.issubdtype(d, np.inexact): return dtypes.finfo(d).bits
  elif dtypes.issubdtype(d, np.integer): return dtypes.iinfo(d).bits
  elif d == np.dtype('bool'): return 1
  else: assert False, d  # should be unreachable, open an issue!

