
def _tmem_store(tmem_addr, shape, num, regs, unpack: bool) -> None:
  num_out_regs, regs_vector = _tmem_access_helper(shape, num)
  pack_mod = ".unpack::16b" if unpack else ""
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [*regs, tmem_addr],
      f"tcgen05.st.sync.aligned.{shape}.x{num}{pack_mod}.b32 [${num_out_regs}], {regs_vector};",
      "r," * num_out_regs + "r",
      has_side_effects=True,
  )

