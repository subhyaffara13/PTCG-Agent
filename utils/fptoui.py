
def fptoui(output: _ods_ir.Type, in_: _ods_ir.Value, rounding_mode: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FPToUIOp(output=output, in_=in_, rounding_mode=rounding_mode, loc=loc, ip=ip).result


def fptoui(out: _ods_ir.Type, in_: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FPToUIOp(out=out, in_=in_, loc=loc, ip=ip).result


def fptoui(res: _ods_ir.Type, arg: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FPToUIOp(res=res, arg=arg, loc=loc, ip=ip).result

