
def unrealized_conversion_cast(outputs: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, UnrealizedConversionCastOp]:
  op = UnrealizedConversionCastOp(outputs=outputs, inputs=inputs, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

