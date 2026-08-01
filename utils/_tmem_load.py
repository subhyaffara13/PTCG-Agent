
def _tmem_load(tmem_addr, shape, num, pack: bool):
  i32 = ir.IntegerType.get_signless(32)
  num_out_regs, regs_vector = _tmem_access_helper(shape, num)
  pack_mod = ".pack::16b" if pack else ""
  if num_out_regs == 1:
    asm_out_ty = i32
  else:
    asm_out_ty = llvm.StructType.get_literal([i32] * num_out_regs)
  regs = llvm.inline_asm(
      asm_out_ty,
      [tmem_addr],
      f"tcgen05.ld.sync.aligned.{shape}.x{num}{pack_mod}.b32 {regs_vector}, [${num_out_regs}];",  # pylint: disable=line-too-long
      "=r," * num_out_regs + "r",
      has_side_effects=True,
  )
  assert isinstance(regs, ir.Value)
  if num_out_regs == 1:
    return [regs]
  else:
    return [llvm.extractvalue(i32, regs, [i]) for i in range(num_out_regs)]

