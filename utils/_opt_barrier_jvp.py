
def _opt_barrier_jvp(primals, tangents):
  tangents = [ad.instantiate_zeros(t) for t in tangents]
  return optimization_barrier(primals), optimization_barrier(tangents)

