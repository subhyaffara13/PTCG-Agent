
def intr_vector_reduce_fmin(res: _ods_ir.Type, in_: _ods_ir.Value[_ods_ir.VectorType], *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return vector_reduce_fmin(res=res, in_=in_, fastmathFlags=fastmath_flags, loc=loc, ip=ip).result

