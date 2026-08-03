import logging

def compute_distributed_to_device_ids(
    devices: Sequence[jax.Device],
) -> list[list[int]]:
  """Returns per-worker device ids in slice-major order."""
  topology = pathways_topology.Topology.from_devices(devices)
  distributed_to_device_ids = [
      list(ids) for ids in topology.distributed_to_device_ids
  ]
  logging.vlog(
      1,
      'Computed Pathways distributed_to_device_ids for %d workers: %s',
      len(distributed_to_device_ids),
      distributed_to_device_ids,
  )
  return distributed_to_device_ids

