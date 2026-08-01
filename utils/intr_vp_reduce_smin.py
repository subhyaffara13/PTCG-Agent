
def intr_vp_reduce_smin(res: _ods_ir.Type, satrt_value: _ods_ir.Value[_ods_ir.IntegerType], val: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPReduceSMinOp(res=res, satrt_value=satrt_value, val=val, mask=mask, evl=evl, loc=loc, ip=ip).result

