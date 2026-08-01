
def _constrain_unreduced(val):
  val_s = core.typeof(val).sharding
  return reshard(val, val_s) if val_s.spec.unreduced else val

