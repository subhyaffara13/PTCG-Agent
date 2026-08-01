
def intr_powi(res: _ods_ir.Type, val: _ods_ir.Value, power: _ods_ir.Value[_ods_ir.IntegerType], *, fastmath_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return PowIOp(res=res, val=val, power=power, fastmathFlags=fastmath_flags, loc=loc, ip=ip).result

