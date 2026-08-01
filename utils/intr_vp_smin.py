
def intr_vp_smin(res: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPSMinOp(res=res, lhs=lhs, rhs=rhs, mask=mask, evl=evl, loc=loc, ip=ip).result

