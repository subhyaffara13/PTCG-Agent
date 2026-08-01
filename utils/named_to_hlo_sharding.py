
def named_to_hlo_sharding(s: NamedSharding | None,
                          aval: core.ShapedArray) -> HloSharding | None:
  if s is None: return None
  return s._to_xla_hlo_sharding(aval.ndim)

