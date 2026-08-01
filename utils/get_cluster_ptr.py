
def get_cluster_ptr(
    ptr: ir.Value, cluster_block: ir.Value, generic: bool = True
):
  i32 = ir.IntegerType.get_signless(32)
  assert cluster_block.type == i32, cluster_block.type
  assert ptr.type == llvm.PointerType.get(3), ptr.type
  mapped_smem_ptr = nvvm.mapa(llvm.PointerType.get(7), ptr, cluster_block)
  if not generic:
    return mapped_smem_ptr
  return llvm.addrspacecast(llvm.PointerType.get(), mapped_smem_ptr)

