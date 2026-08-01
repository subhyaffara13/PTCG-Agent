
def memory_space_cast(dest: _ods_ir.Type, source: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MemorySpaceCastOp(dest=dest, source=source, loc=loc, ip=ip).result

