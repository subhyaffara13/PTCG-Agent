
def distinct_objects(operands_: _Sequence[_ods_ir.Value[_ods_ir.MemRefType]], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, DistinctObjectsOp]:
  op = DistinctObjectsOp(operands_=operands_, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

