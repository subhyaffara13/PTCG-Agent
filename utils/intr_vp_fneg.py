
def intr_vp_fneg(res: _ods_ir.Type, op: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPFNegOp(res=res, op=op, mask=mask, evl=evl, loc=loc, ip=ip).result

