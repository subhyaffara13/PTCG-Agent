
def ptr_as_memref(ptr, memref_ty: ir.MemRefType):
  ptr_ty = llvm.PointerType(ptr.type)
  if ptr_ty.address_space != (get_memref_llvm_address_space(memref_ty) or 0):
    raise ValueError(
        f"Pointer address space {ptr_ty.address_space} does not match "
        f"memref memory space {memref_ty.memory_space}."
    )

  strides, offset = memref_ty.get_strides_and_offset()
  if offset != 0:
    raise ValueError("Non-zero offset is not supported for ptr_as_memref")
  i64 = ir.IntegerType.get_signless(64)
  rank = len(memref_ty.shape)
  desc_ty_fields = [ptr_ty, ptr_ty, i64]
  if rank > 0:
    desc_ty_fields += [llvm.ArrayType.get(i64, rank)] * 2
  desc_ty = llvm.StructType.get_literal(desc_ty_fields)
  desc = llvm.UndefOp(desc_ty).result
  desc = llvm.InsertValueOp(desc, ptr, [0]).result  # Allocation
  desc = llvm.InsertValueOp(desc, ptr, [1]).result  # Aligned Base
  desc = llvm.InsertValueOp(
      desc, llvm.ConstantOp(i64, ir.IntegerAttr.get(i64, 0)).result, [2]
  ).result
  if rank > 0:
    for i, s in enumerate(memref_ty.shape):
      desc = llvm.InsertValueOp(
          desc, llvm.ConstantOp(i64, ir.IntegerAttr.get(i64, s)).result, [3, i]
      ).result
    for i, s in enumerate(strides):
      desc = llvm.InsertValueOp(
          desc, llvm.ConstantOp(i64, ir.IntegerAttr.get(i64, s)).result, [4, i]
      ).result
  result = builtin.unrealized_conversion_cast([memref_ty], [desc])
  assert isinstance(result, ir.Value)
  return result

