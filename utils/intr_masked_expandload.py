
def intr_masked_expandload(res: _ods_ir.Type, ptr: _ods_ir.Value, mask: _ods_ir.Value[_ods_ir.VectorType], passthru: _ods_ir.Value[_ods_ir.VectorType], *, arg_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, res_attrs: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return masked_expandload(res=res, ptr=ptr, mask=mask, passthru=passthru, arg_attrs=arg_attrs, res_attrs=res_attrs, loc=loc, ip=ip).result

