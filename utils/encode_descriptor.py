
def encode_descriptor(
    ref_arg,
    leading_byte_offset: int,
    stride_byte_offset: int,
    swizzle: int | mgpu_dialect.SwizzlingMode | None,
    const_init: int = 0,
    split_const: bool = False,
):
  i32 = ir.IntegerType.get_signless(32)
  i64 = ir.IntegerType.get_signless(64)
  if isinstance(ref_arg.type, ir.MemRefType):
    ptr = utils.memref_ptr(ref_arg)
  else:
    ptr = ref_arg
  assert ptr.type == llvm.PointerType.get(address_space=3), ptr.type
  ptr_val = llvm.ptrtoint(i64, ptr)
  c = lambda x: arith.constant(i64, x)
  if swizzle is None or swizzle == mgpu_dialect.SwizzlingMode.kNoSwizzle:
    swizzle_encoding = 0
  elif swizzle == mgpu_dialect.SwizzlingMode.k128ByteSwizzle:
    swizzle_encoding = 1
  elif swizzle == mgpu_dialect.SwizzlingMode.k64ByteSwizzle:
    swizzle_encoding = 2
  elif swizzle == mgpu_dialect.SwizzlingMode.k32ByteSwizzle:
    swizzle_encoding = 3
  else:
    raise NotImplementedError(swizzle)
  encoded_base_addr = llvm.lshr(llvm.and_(ptr_val, c(0x3FFFF)), c(4))
  # We ignore the offset
  desc_const = (
      const_init
      | (encode_addr(leading_byte_offset) << 16)
      | (encode_addr(stride_byte_offset) << 32)
      | (swizzle_encoding << 62)
  )
  if split_const:
    # The encoded base addr fits within a single 32-bit register.
    return arith.trunci(i32, encoded_base_addr), desc_const
  else:
    # The desc_const frequently has the MSB set, leading to errors when trying
    # to create ir.IntegerAttr through the MLIR python bindings... This should
    # be easy enough for LLVM to constant fold away.
    if desc_const >> 63:
      desc_val = c(desc_const & 0xFFFFFFFF)
      desc_val = llvm.or_(desc_val, arith.shli(c(desc_const >> 32), c(32)))
    else:
      desc_val = c(desc_const)
    return llvm.or_(encoded_base_addr, desc_val)

