
def unary(self: list[int]):
    return _copy(self)


def unary(output: _ods_ir.Type, x: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UnaryOp(output=output, x=x, loc=loc, ip=ip).result

