
def tcgen05_mma_smem_desc(start_addr: _ods_ir.Value[_ods_ir.IntegerType], leading_dim_offset: _ods_ir.Value[_ods_ir.IntegerType], stride_dim_offset: _ods_ir.Value[_ods_ir.IntegerType], base_offset: _ods_ir.Value[_ods_ir.IntegerType], leading_dim_mode: _ods_ir.Value[_ods_ir.IntegerType], swizzle_mode: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return Tcgen05MmaSmemDescOp(startAddr=start_addr, leadingDimOffset=leading_dim_offset, strideDimOffset=stride_dim_offset, baseOffset=base_offset, leadingDimMode=leading_dim_mode, swizzleMode=swizzle_mode, results=results, loc=loc, ip=ip).result

