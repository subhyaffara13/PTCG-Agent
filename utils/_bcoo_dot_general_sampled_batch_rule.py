
def _bcoo_dot_general_sampled_batch_rule(batched_args, batch_dims, *, dimension_numbers):
  def impl(A, B, indices):
    return _bcoo_dot_general_sampled_impl(A, B, indices, dimension_numbers=dimension_numbers)
  return vmap(impl, in_axes=batch_dims, out_axes=0)(*batched_args), 0

