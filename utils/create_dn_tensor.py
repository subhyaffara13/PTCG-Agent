
def create_dn_tensor(dn_tensor: _ods_ir.Type, async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], memref: _ods_ir.Value[_ods_ir.MemRefType], dims: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CreateDnTensorOp]:
  op = CreateDnTensorOp(dnTensor=dn_tensor, asyncToken=async_token, asyncDependencies=async_dependencies, memref=memref, dims=dims, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

