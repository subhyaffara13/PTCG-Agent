
def _wgmma_accumulator_deref_discharge(in_avals, out_avals, acc, *, wait_n):
  del in_avals, out_avals
  return (None,), wgmma_accumulator_deref_p.bind(acc, wait_n=wait_n)

