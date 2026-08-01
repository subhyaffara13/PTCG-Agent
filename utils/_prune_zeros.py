
def _prune_zeros(ts):
  return [t for t in ts if type(t) is not ad_util.Zero]

