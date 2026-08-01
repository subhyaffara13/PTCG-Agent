
def intr_get_active_lane_mask(res: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.IntegerType], n: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return GetActiveLaneMaskOp(res=res, base=base, n=n, loc=loc, ip=ip).result

