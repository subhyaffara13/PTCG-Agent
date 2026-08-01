
def intr_vector_reduce_smax(res: _ods_ir.Type, in_: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return vector_reduce_smax(res=res, in_=in_, loc=loc, ip=ip).result

