
def offload_dot_with_no_batch_dims(offload_src, offload_dst):
  """Same as ``dots_with_no_batch_dims_saveable``, but offload to CPU memory
  instead of recomputing.

  This is a useful heuristic for transformers."""
  def policy(prim, *_, **params):
    if prim is lax_internal.dot_general_p:
      (_, _), (lhs_b, rhs_b) = params['dimension_numbers']
      if not lhs_b and not rhs_b:
        return pe.Offloadable(src=offload_src, dst=offload_dst)
    return pe.Recompute
  return policy

