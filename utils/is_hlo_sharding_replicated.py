
def is_hlo_sharding_replicated(hc: xc.HloSharding) -> bool:
  return True if hc.num_devices() == 1 else hc.is_replicated()

