
def smem() -> ir.Attribute:
  """Returns the attribute for the SMEM memory space."""
  return ir.Attribute.parse("#gpu.address_space<workgroup>")

