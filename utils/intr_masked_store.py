
def intr_masked_store(value: _ods_ir.Value[_ods_ir.VectorType], data: _ods_ir.Value, mask: _ods_ir.Value[_ods_ir.VectorType], alignment: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MaskedStoreOp:
  return MaskedStoreOp(value=value, data=data, mask=mask, alignment=alignment, loc=loc, ip=ip)

