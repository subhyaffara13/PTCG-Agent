
def tmem() -> ir.Attribute:
  """Returns the attribute for the TMEM memory space."""
  return ir.Attribute.parse("#mosaic_gpu.tmem")

