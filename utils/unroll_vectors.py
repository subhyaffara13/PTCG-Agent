
def unroll_vectors(output: _Sequence[_ods_ir.Type], input: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, UnrollVectorsOp]:
  op = UnrollVectorsOp(output=output, input=input, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

