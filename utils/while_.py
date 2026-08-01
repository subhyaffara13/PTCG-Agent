
def while_(result: _Sequence[_ods_ir.Type], operand: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, WhileOp]:
  op = WhileOp(result=result, operand=operand, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def while_(results_: _Sequence[_ods_ir.Type], inits: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, WhileOp]:
  op = WhileOp(results_=results_, inits=inits, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def while_(result: _Sequence[_ods_ir.Type], operand: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, WhileOp]:
  op = WhileOp(result=result, operand=operand, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

