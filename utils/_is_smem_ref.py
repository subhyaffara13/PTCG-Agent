
def _is_smem_ref(v: ir.Value) -> bool:
  return isinstance(v.type, ir.MemRefType) and (
      utils.is_smem_ref(v) or utils.is_cluster_smem_ref(v)
  )

