
def _wgmma_ref_discharge(in_avals, out_avals, *args, **kwargs):
  del in_avals, out_avals
  return (wgmma_p.bind(*args, **kwargs), *([None] * (len(args) - 1))), []

