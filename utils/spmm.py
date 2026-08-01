
def spmm(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], spmat_a: _ods_ir.Value, dnmat_b: _ods_ir.Value, dnmat_c: _ods_ir.Value, compute_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], buffers: _Sequence[_ods_ir.Value[_ods_ir.MemRefType]], *, mode_a: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, mode_b: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, SpMMOp]:
  op = SpMMOp(asyncToken=async_token, asyncDependencies=async_dependencies, spmatA=spmat_a, dnmatB=dnmat_b, dnmatC=dnmat_c, computeType=compute_type, buffers=buffers, modeA=mode_a, modeB=mode_b, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

