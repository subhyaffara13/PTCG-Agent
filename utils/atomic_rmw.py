
def atomic_rmw(result: _ods_ir.Type, atomic_rmw_op: _Union[_Any, _ods_ir.Attribute], ptr: _ods_ir.Value, val: _ods_ir.Value, sem: _Union[_Any, _ods_ir.Attribute], scope: _Union[_Any, _ods_ir.Attribute], *, mask: _Optional[_ods_ir.Value] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtomicRMWOp(result=result, atomic_rmw_op=atomic_rmw_op, ptr=ptr, val=val, sem=sem, scope=scope, mask=mask, loc=loc, ip=ip).result


def atomic_rmw(kind: _Union[_Any, _ods_ir.Attribute], value: _ods_ir.Value, memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtomicRMWOp(kind=kind, value=value, memref=memref, indices=indices, results=results, loc=loc, ip=ip).result

