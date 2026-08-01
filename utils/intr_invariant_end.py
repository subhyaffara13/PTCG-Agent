
def intr_invariant_end(start: _ods_ir.Value, size: _Union[int, _ods_ir.IntegerAttr], ptr: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> InvariantEndOp:
  return InvariantEndOp(start=start, size=size, ptr=ptr, loc=loc, ip=ip)

