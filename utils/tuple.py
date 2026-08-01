
def tuple(val: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TupleOp(val=val, results=results, loc=loc, ip=ip).result


def tuple(val: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TupleOp(val=val, results=results, loc=loc, ip=ip).result


def tuple(*elements):
    return TupleType.get_tuple(elements)

