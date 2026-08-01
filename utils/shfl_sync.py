
def shfl_sync(thread_mask: _ods_ir.Value[_ods_ir.IntegerType], val: _ods_ir.Value, offset: _ods_ir.Value[_ods_ir.IntegerType], mask_and_clamp: _ods_ir.Value[_ods_ir.IntegerType], kind: _Union[_Any, _ods_ir.Attribute], *, return_value_and_is_valid: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ShflOp(thread_mask=thread_mask, val=val, offset=offset, mask_and_clamp=mask_and_clamp, kind=kind, return_value_and_is_valid=return_value_and_is_valid, results=results, loc=loc, ip=ip).result

