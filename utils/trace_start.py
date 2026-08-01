
def trace_start(message: _Union[str, _ods_ir.StringAttr], level: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TraceStartOp:
  return TraceStartOp(message=message, level=level, loc=loc, ip=ip)

