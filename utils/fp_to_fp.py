
def fp_to_fp(result: _ods_ir.Type, src: _ods_ir.Value, *, rounding: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FpToFpOp(result=result, src=src, rounding=rounding, loc=loc, ip=ip).result

