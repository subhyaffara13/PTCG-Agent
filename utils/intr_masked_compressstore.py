
def intr_masked_compressstore(value: _ods_ir.Value[_ods_ir.VectorType], ptr: _ods_ir.Value, mask: _ods_ir.Value[_ods_ir.VectorType], *, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> masked_compressstore:
  return masked_compressstore(value=value, ptr=ptr, mask=mask, arg_attrs=arg_attrs, res_attrs=res_attrs, loc=loc, ip=ip)

