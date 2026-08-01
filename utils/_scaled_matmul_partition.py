
def _scaled_matmul_partition(
    preferred_element_type, mesh, shapes, output_shape
  ):
  shardings = tree_util.tree_map(lambda x: x.sharding, shapes)
  _check_shardings(shardings)

  lhs, rhs = shardings[0], shardings[1]
  out = output_shape[0].sharding
  use_all_reduce = _enable_all_reduce(lhs, rhs)
  reduce_scatter_dim = _get_reduce_scatter_dim(lhs, rhs, out)
  lhs_k_spec = lhs.spec[2]

  def _scaled_matmul_impl_partition(a, b, a_scale, b_scale):
    z = _scaled_matmul_impl(a, b, a_scale, b_scale, preferred_element_type)
    if reduce_scatter_dim is not None:
      z = lax_parallel.psum_scatter(
          z, lhs_k_spec, scatter_dimension=reduce_scatter_dim, tiled=True
      )
    elif use_all_reduce:
      z = lax_parallel.psum(z, lhs_k_spec)
    return z

  arg_shardings, out_shardings = _supported_in_out_sharding(lhs, rhs, out, reduce_scatter_dim)
  return mesh, _scaled_matmul_impl_partition, out_shardings, arg_shardings

