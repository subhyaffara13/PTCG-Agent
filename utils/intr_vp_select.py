
def intr_vp_select(res: _ods_ir.Type, cond: _ods_ir.Value[_ods_ir.VectorType], true_val: _ods_ir.Value[_ods_ir.VectorType], false_val: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPSelectMinOp(res=res, cond=cond, true_val=true_val, false_val=false_val, evl=evl, loc=loc, ip=ip).result

