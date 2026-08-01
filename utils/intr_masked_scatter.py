
def intr_masked_scatter(value: _ods_ir.Value[_ods_ir.VectorType], ptrs: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], alignment: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> masked_scatter:
  return masked_scatter(value=value, ptrs=ptrs, mask=mask, alignment=alignment, loc=loc, ip=ip)

