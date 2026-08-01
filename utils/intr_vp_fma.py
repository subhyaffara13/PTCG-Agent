
def intr_vp_fma(res: _ods_ir.Type, op1: _ods_ir.Value[_ods_ir.VectorType], op2: _ods_ir.Value[_ods_ir.VectorType], op3: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPFmaOp(res=res, op1=op1, op2=op2, op3=op3, mask=mask, evl=evl, loc=loc, ip=ip).result

