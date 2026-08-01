
def intr_experimental_vp_strided_store(val: _ods_ir.Value[_ods_ir.VectorType], ptr: _ods_ir.Value, stride: _ods_ir.Value[_ods_ir.IntegerType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VPStridedStoreOp:
  return VPStridedStoreOp(val=val, ptr=ptr, stride=stride, mask=mask, evl=evl, loc=loc, ip=ip)

