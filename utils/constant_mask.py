
def constant_mask(result: _ods_ir.Type, mask_dim_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ConstantMaskOp(result=result, mask_dim_sizes=mask_dim_sizes, loc=loc, ip=ip).result

