
def _has_non_replicated_sharding_sdy(op: ir.Operation) -> bool:
  try:
    sharding = op.attributes["sharding"]
  except KeyError:
    return False
  return not _is_replicated_sdy(sharding)

