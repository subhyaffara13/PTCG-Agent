
def broadcast_compare(lhs: _ods_ir.Value, rhs: _ods_ir.Value, comparison_direction: _Union[_Any, _ods_ir.Attribute], *, broadcast_dimensions: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, compare_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BroadcastCompareOp(lhs=lhs, rhs=rhs, comparison_direction=comparison_direction, broadcast_dimensions=broadcast_dimensions, compare_type=compare_type, results=results, loc=loc, ip=ip).result

