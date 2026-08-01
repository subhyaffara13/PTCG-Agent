
def convertf(out: _ods_ir.Type, in_: _ods_ir.Value, *, roundingmode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConvertFOp(out=out, in_=in_, roundingmode=roundingmode, fastmath=fastmath, loc=loc, ip=ip).result

