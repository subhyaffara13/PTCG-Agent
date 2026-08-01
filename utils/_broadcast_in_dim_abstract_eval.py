
def _broadcast_in_dim_abstract_eval(x, shape, broadcast_dimensions,
                                    sharding):
  shape = _broadcast_in_dim_shape_rule(  # error checking
      x, shape=shape, broadcast_dimensions=broadcast_dimensions, sharding=None)
  new_sharding = _broadcast_in_dim_sharding_rule(
      x, shape=shape, broadcast_dimensions=broadcast_dimensions,
      sharding=sharding)
  new_vma = core.standard_vma_rule('broadcast_in_dim', x)
  out_mat = x.mat.update(varying=new_vma)
  out_aval = core.ShapedArray(shape, x.dtype, x.weak_type, sharding=new_sharding,
                              manual_axis_type=out_mat,
                              memory_space=x.memory_space)
  core.check_avals_context_mesh([out_aval], 'broadcast_in_dim')
  return out_aval

