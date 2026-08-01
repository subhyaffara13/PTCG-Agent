
def clampf(x: _ods_ir.Value, min: _ods_ir.Value, max: _ods_ir.Value, propagate_nan: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ClampFOp(x=x, min=min, max=max, propagateNan=propagate_nan, results=results, loc=loc, ip=ip).result


def clampf(value: _ods_ir.Value, min: _ods_ir.Value, max: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ClampFOp(value=value, min=min, max=max, fastmath=fastmath, results=results, loc=loc, ip=ip).result

