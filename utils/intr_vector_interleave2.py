
def intr_vector_interleave2(res: _ods_ir.Type, vec1: _ods_ir.Value[_ods_ir.VectorType], vec2: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return vector_interleave2(res=res, vec1=vec1, vec2=vec2, loc=loc, ip=ip).result

