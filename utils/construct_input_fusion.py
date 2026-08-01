
def construct_input_fusion(
    candidate_values, jaxpr: jax_core.Jaxpr, outvars
) -> fusion_lib.Fusion:
  new_jaxpr, new_values, in_type, out_type, out_tree = _construct_fusion_jaxpr(
      candidate_values, jaxpr, outvars,
  )

  def _fn():
    out_flat = jax_core.eval_jaxpr(new_jaxpr, new_values)
    return tree_util.tree_unflatten(out_tree, out_flat)

  return fusion_lib.Fusion(_fn, in_type, out_type)

