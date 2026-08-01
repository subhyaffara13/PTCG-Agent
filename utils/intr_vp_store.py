
def intr_vp_store(val: _ods_ir.Value[_ods_ir.VectorType], ptr: _ods_ir.Value, mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VPStoreOp:
  return VPStoreOp(val=val, ptr=ptr, mask=mask, evl=evl, loc=loc, ip=ip)

