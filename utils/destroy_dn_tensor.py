
def destroy_dn_tensor(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], dn_tensor: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, DestroyDnTensorOp]:
  op = DestroyDnTensorOp(asyncToken=async_token, asyncDependencies=async_dependencies, dnTensor=dn_tensor, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

