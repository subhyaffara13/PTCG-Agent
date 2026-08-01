
def is_transformable_smem_memref(v: ir.Value) -> bool:
  """Whether the value is a memref in SMEM on which transforms should be applied."""
  return (
      isinstance(v.type, ir.MemRefType)
      # barriers have no business being transformed
      and not isinstance(v.type.element_type, mgpu.BarrierType)
      and (utils.is_smem_ref(v) or utils.is_cluster_smem_ref(v))
  )

