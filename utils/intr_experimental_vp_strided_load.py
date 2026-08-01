
def intr_experimental_vp_strided_load(res: _ods_ir.Type, ptr: _ods_ir.Value, stride: _ods_ir.Value[_ods_ir.IntegerType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPStridedLoadOp(res=res, ptr=ptr, stride=stride, mask=mask, evl=evl, loc=loc, ip=ip).result

