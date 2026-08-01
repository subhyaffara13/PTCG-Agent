
def intr_vector_deinterleave2(res: _ods_ir.Type, vec: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return vector_deinterleave2(res=res, vec=vec, loc=loc, ip=ip).result

