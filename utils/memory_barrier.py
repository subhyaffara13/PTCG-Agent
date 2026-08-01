
def memory_barrier(scope: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MembarOp:
  return MembarOp(scope=scope, loc=loc, ip=ip)

