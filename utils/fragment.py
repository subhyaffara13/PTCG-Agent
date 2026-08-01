
def fragment(results_: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], origin: _Union[_Any, _ods_ir.ArrayAttr], mesh_name: _Union[str, _ods_ir.StringAttr], *, stage_id: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, in_shardings: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, out_shardings: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, FragmentOp]:
  op = FragmentOp(results_=results_, inputs=inputs, origin=origin, mesh_name=mesh_name, stage_id=stage_id, in_shardings=in_shardings, out_shardings=out_shardings, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

