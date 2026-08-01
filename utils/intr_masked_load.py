
def intr_masked_load(res: _ods_ir.Type, data: _ods_ir.Value, mask: _ods_ir.Value[_ods_ir.VectorType], alignment: _Union[int, _ods_ir.IntegerAttr], *, pass_thru: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, nontemporal: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MaskedLoadOp(res=res, data=data, mask=mask, alignment=alignment, pass_thru=pass_thru, nontemporal=nontemporal, loc=loc, ip=ip).result

