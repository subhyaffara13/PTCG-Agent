
def _opt_barrier_transpose(cts, *primals):
  cts = [ad.instantiate_zeros(ct) for ct in cts]
  return optimization_barrier(cts)

