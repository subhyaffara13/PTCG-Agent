
def intr_vp_inttoptr(res: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], evl: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VPIntToPtrOp(res=res, src=src, mask=mask, evl=evl, loc=loc, ip=ip).result

