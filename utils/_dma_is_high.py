
def _dma_is_high(*avals, **params):
  return any(aval.is_high for aval in avals)

