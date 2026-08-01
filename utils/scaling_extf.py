
def scaling_extf(out: _ods_ir.Type, in_: _ods_ir.Value, scale: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ScalingExtFOp(out=out, in_=in_, scale=scale, fastmath=fastmath, loc=loc, ip=ip).result

