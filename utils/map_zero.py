
def map_zero(axis_data, d, ct):
  if isinstance(ct, ad_util.Zero):
    return ad_util.Zero(core.mapped_aval(axis_data.size, d, ct.aval))
  return ct

