
def device_async_create_group(input_tokens: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DeviceAsyncCreateGroupOp(inputTokens=input_tokens, results=results, loc=loc, ip=ip).result

