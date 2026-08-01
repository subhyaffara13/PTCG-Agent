
def intr_vector_extract(res: _ods_ir.Type, srcvec: _ods_ir.Value[_ods_ir.VectorType], pos: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return vector_extract(res=res, srcvec=srcvec, pos=pos, loc=loc, ip=ip).result

