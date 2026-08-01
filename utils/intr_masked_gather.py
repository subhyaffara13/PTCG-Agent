
def intr_masked_gather(res: _ods_ir.Type, ptrs: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], pass_thru: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], alignment: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return masked_gather(res=res, ptrs=ptrs, mask=mask, pass_thru=pass_thru, alignment=alignment, loc=loc, ip=ip).result

