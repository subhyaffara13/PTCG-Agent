
def _has_non_replicated_sharding_mhlo(op: ir.Operation) -> bool:
  try:
    sharding = op.attributes["mhlo.sharding"]
  except KeyError:
    return False
  try:
    sharding_value = ir.StringAttr(sharding).value
  except UnicodeDecodeError:
    # The mhlo.sharding attribute may be in pretty-printed format, or
    # as an encoding of an HloSharding protobuf in some rare situations.
    # We handle the latter by conservatively assuming it is non-replicated.
    return True
  else:
    return not check_sharding_pattern.match(sharding_value)

