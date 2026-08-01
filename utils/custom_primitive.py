
def custom_primitive(result: _Sequence[_ods_ir.Type], operands_: _Sequence[_ods_ir.Value], in_layouts: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], in_transforms: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], out_layouts: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CustomPrimitiveOp]:
  op = CustomPrimitiveOp(result=result, operands_=operands_, in_layouts=in_layouts, in_transforms=in_transforms, out_layouts=out_layouts, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

