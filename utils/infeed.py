
def infeed(result: _Sequence[_ods_ir.Type], token: _ods_ir.Value, *, infeed_config: _Optional[_Union[str, _ods_ir.StringAttr]] = None, layout: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, InfeedOp]:
  op = InfeedOp(result=result, token=token, infeed_config=infeed_config, layout=layout, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def infeed(result: _Sequence[_ods_ir.Type], token: _ods_ir.Value, *, infeed_config: _Optional[_Union[str, _ods_ir.StringAttr]] = None, layout: _Optional[_Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, InfeedOp]:
  op = InfeedOp(result=result, token=token, infeed_config=infeed_config, layout=layout, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

