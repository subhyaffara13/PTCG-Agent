
def inline_ptx(write_only_args: _Sequence[_ods_ir.Type], read_only_args: _Sequence[_ods_ir.Value], read_write_args: _Sequence[_ods_ir.Value], ptx_code: _Union[str, _ods_ir.StringAttr], *, predicate: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, InlinePtxOp]:
  op = InlinePtxOp(writeOnlyArgs=write_only_args, readOnlyArgs=read_only_args, readWriteArgs=read_write_args, ptxCode=ptx_code, predicate=predicate, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def inline_ptx(asm: str):
  """Inserts inline PTX assembly."""

  @gpu_primitives.inline_mgpu()
  def ptx(_):
    void = ir.Type.parse("!llvm.void")
    llvm.inline_asm(void, [], asm, "", has_side_effects=True)

  ptx()

