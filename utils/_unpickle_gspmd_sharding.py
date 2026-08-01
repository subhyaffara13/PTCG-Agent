
def _unpickle_gspmd_sharding(devices, op_sharding, memory_kind):
  return GSPMDSharding(devices, op_sharding, memory_kind=memory_kind)

