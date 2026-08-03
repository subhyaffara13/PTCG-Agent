from typing import Set

def get_primary_replica_ids_and_pids(
    replica_axis_idx: int,
    mesh: jax.sharding.Mesh,
    primary_replica_id: int,
) -> tuple[Set[int], Set[int]]:
  """Returns the primary replica ids and process ids."""
  devices = replica_devices(
      mesh,
      replica_id=primary_replica_id,
      replica_axis_index=replica_axis_idx,
  ).flatten()
  ids = set([d.id for d in devices])
  pids = multihost.unique_processes_from_devices(devices)
  return ids, pids

