
def fpext(res: _ods_ir.Type, arg: _ods_ir.Value, *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FPExtOp(res=res, arg=arg, fastmathFlags=fastmath_flags, loc=loc, ip=ip).result

