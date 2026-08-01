
def intr_frexp(res: _ods_ir.Type, val: _ods_ir.Value, *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FractionExpOp(res=res, val=val, fastmathFlags=fastmath_flags, loc=loc, ip=ip).result

