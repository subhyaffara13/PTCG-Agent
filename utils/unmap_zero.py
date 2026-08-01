
def unmap_zero(axis_data, d, ct):
  if isinstance(ct, ad_util.Zero):
    return ad_util.Zero(core.unmapped_aval(axis_data.size, d, ct.aval,
                                           axis_data.explicit_mesh_axis))
  return ct

