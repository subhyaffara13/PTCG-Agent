
def call_indirect(results_: _Sequence[_ods_ir.Type], callee: _ods_ir.Value, callee_operands: _Sequence[_ods_ir.Value], *, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CallIndirectOp]:
  op = CallIndirectOp(results_=results_, callee=callee, callee_operands=callee_operands, arg_attrs=arg_attrs, res_attrs=res_attrs, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

