
def are_hlo_shardings_equal(hc1: xc.HloSharding, hc2: xc.HloSharding) -> bool:
  if hc1 is hc2:
    return True
  if is_hlo_sharding_replicated(hc1) and is_hlo_sharding_replicated(hc2):
    return True
  return hc1 == hc2

