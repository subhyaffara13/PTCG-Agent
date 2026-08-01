
def fragment_call(result: _Sequence[_ods_ir.Type], tensors: _Sequence[_ods_ir.Value], origin: _Union[_Any, _ods_ir.ArrayAttr], mesh_name: _Union[str, _ods_ir.StringAttr], callee: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, FragmentCallOp]:
  op = FragmentCallOp(result=result, tensors=tensors, origin=origin, mesh_name=mesh_name, callee=callee, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

