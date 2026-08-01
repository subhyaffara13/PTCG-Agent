
def is_cluster_smem_ref(ref: ir.Value | ir.Type) -> bool:
  """Returns true if the input mem ref or memref type points to cluster SMEM."""
  if isinstance(ref, ir.Value):
    ref = ref.type
  if not isinstance(ref, ir.MemRefType):
    raise ValueError(f"Expected a memref type but got {ref}")
  ref = ir.MemRefType(ref)
  return ref.memory_space is not None and ref.memory_space == smem_cluster()

