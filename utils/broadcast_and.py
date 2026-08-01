
def broadcast_and(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, broadcast_dimensions: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BroadcastAndOp(lhs=lhs, rhs=rhs, broadcast_dimensions=broadcast_dimensions, results=results, loc=loc, ip=ip).result

