
def _is_host_for_primary_replica(primary_replica_ids: set[int]) -> bool:
  return multihost.process_index() in primary_replica_ids

