
def smem_cluster() -> ir.Attribute:
  """Returns the attribute for the cluster SMEM memory space."""
  return ir.Attribute.parse("#mosaic_gpu.smem_cluster")

