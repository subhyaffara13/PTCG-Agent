
def _wgmma_accumulator_store_discharge(in_avals, out_avals, acc, val):
  del in_avals, out_avals
  return (wgmma_accumulator_store_p.bind(acc, val), None), []

