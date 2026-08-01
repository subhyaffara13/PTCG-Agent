
def get_memref_llvm_address_space(memref_ty: ir.MemRefType) -> int | None:
  if (memory_space := memref_ty.memory_space) is None:
    return None
  if isinstance(memory_space, ir.IntegerAttr):
    return memory_space.value
  return gpu_address_space_to_nvptx(_MEMORY_SPACES[str(memory_space)])

