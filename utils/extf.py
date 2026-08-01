
def extf(out: _ods_ir.Type, in_: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExtFOp(out=out, in_=in_, loc=loc, ip=ip).result


def extf(out: _ods_ir.Type, in_: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExtFOp(out=out, in_=in_, fastmath=fastmath, loc=loc, ip=ip).result

