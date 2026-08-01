
def execute_region(result: _Sequence[_ods_ir.Type], *, no_inline: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ExecuteRegionOp]:
  op = ExecuteRegionOp(result=result, no_inline=no_inline, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

