
def fusion(results_: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], *, fusion_kind: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, output_operand_aliases: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, FusionOp]:
  op = FusionOp(results_=results_, inputs=inputs, fusion_kind=fusion_kind, output_operand_aliases=output_operand_aliases, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

