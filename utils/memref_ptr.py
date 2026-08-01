
def memref_ptr(memref_arg):
  i64 = ir.IntegerType.get_signless(64)
  memref_ty = ir.MemRefType(memref_arg.type)
  rank = len(memref_ty.shape)
  address_space = get_memref_llvm_address_space(memref_ty)
  ptr_ty = llvm.PointerType.get(address_space)
  desc_ty_fields = [ptr_ty, ptr_ty, i64]
  if rank > 0:
    desc_ty_fields += [llvm.ArrayType.get(i64, rank)] * 2
  desc_ty = llvm.StructType.get_literal(desc_ty_fields)
  desc = builtin.unrealized_conversion_cast([desc_ty], [memref_arg])
  assert isinstance(desc, ir.Value)
  aligned_ptr = llvm.extractvalue(ptr_ty, desc, [1])
  offset_elems = llvm.extractvalue(i64, desc, [2])

  elem_bitwidth = bitwidth(memref_ty.element_type)
  if elem_bitwidth < 8:
    *_, static_offset = memref_ty.get_strides_and_offset()
    if static_offset != ir.ShapedType.get_dynamic_stride_or_offset():
      assert elem_bitwidth.bit_count() == 1
      packing = 8 // elem_bitwidth
      if static_offset % packing != 0:
        raise ValueError(
            f"{memref_ty} {static_offset=} is not divisible by {packing=}`"
        )
      offset_bytes = c(static_offset // packing, i64)
    else:
      offset_bits = llvm.mul(
          offset_elems,
          c(elem_bitwidth, i64),
          overflow_flags=llvm.IntegerOverflowFlags.none,
      )
      offset_bytes = llvm.udiv(offset_bits, c(8, i64))
  else:
    assert elem_bitwidth % 8 == 0
    offset_bytes = llvm.mul(
        offset_elems,
        c(elem_bitwidth // 8, i64),
        overflow_flags=llvm.IntegerOverflowFlags.none,
    )
  return llvm.inttoptr(
      ptr_ty,
      llvm.add(
          llvm.ptrtoint(i64, aligned_ptr),
          offset_bytes,
          overflow_flags=llvm.IntegerOverflowFlags.none,
      ),
  )

