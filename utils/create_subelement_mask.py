
def create_subelement_mask(output: _ods_ir.Type, from_: _Union[int, _ods_ir.IntegerAttr], to: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CreateSubelementMaskOp(output=output, from_=from_, to=to, loc=loc, ip=ip).result

