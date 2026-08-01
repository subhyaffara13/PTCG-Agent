
def _tmem_addr_to_ptr(tmem_addr: ir.Value) -> ir.Value:
  assert tmem_addr.type == ir.IntegerType.get_signless(32)
  return llvm.inttoptr(llvm.PointerType.get(address_space=6), tmem_addr)

