
def bar_warp_sync(mask: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> SyncWarpOp:
  return SyncWarpOp(mask=mask, loc=loc, ip=ip)

