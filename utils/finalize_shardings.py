
def finalize_shardings(shardings, device_assignment):
  if len(device_assignment) == 1:
    return [make_single_device_sharding(device_assignment[0], memory_kind=o.memory_kind)
            if isinstance(o, GSPMDSharding) else o for o in shardings]
  return shardings

