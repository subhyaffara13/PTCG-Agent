
def getelementptr(res: _ods_ir.Type, base: _ods_ir.Value, dynamic_indices: _Sequence[_ods_ir.Value], raw_constant_indices: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], elem_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], no_wrap_flags, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return GEPOp(res=res, base=base, dynamicIndices=dynamic_indices, rawConstantIndices=raw_constant_indices, elem_type=elem_type, noWrapFlags=no_wrap_flags, loc=loc, ip=ip).result


def getelementptr(
    ptr: ir.Value, indices: Sequence[ir.Value | int], dtype: ir.Type
) -> ir.Value:
  static_indices = [i if isinstance(i, int) else DYNAMIC32 for i in indices]
  dyn_indices = [i for i in indices if not isinstance(i, int)]
  return llvm.getelementptr(
      ptr.type,
      ptr,
      dyn_indices,
      static_indices,
      dtype,
      llvm.GEPNoWrapFlags.none,
  )

