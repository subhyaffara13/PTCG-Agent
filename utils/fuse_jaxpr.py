
def fuse_jaxpr(
    jaxpr: jax_core.Jaxpr, out_tree: tree_util.PyTreeDef, consts, *args,
    strict_mode: bool = True,
):
  # Collect input fusions
  fusion_eqn_index = None
  for i, eqn in enumerate(jaxpr.eqns):
    if eqn.primitive is fusible_p:
      fusion_eqn_index = i
      break
  if fusion_eqn_index is None:
    raise ValueError("No fusible eqn found")
  fusion_eqn = jaxpr.eqns[fusion_eqn_index]

  # Now let's check if we need to do any fusion at all, e.g. do the outputs of
  # the jaxpr have any dependence on the fusion at all?
  candidate_values = [*consts, *args]
  jaxpr_without_fusible = jaxpr.replace(
      eqns=(jaxpr.eqns[:fusion_eqn_index]
                + jaxpr.eqns[fusion_eqn_index + 1 :]),
      constvars=jaxpr.constvars + jaxpr.invars,
      invars=fusion_eqn.outvars,
      debug_info=jaxpr.debug_info.with_unknown_names())
  discharged_jaxpr_without_fusible, *_ = (
      fuser_utils.discharge_state(jaxpr_without_fusible))
  independent_jaxpr, _, out_used, *_ = pe.partial_eval_jaxpr_custom(
      discharged_jaxpr_without_fusible,
      in_unknowns=[True] * len(fusion_eqn.outvars),
      in_inst=[True] * len(fusion_eqn.outvars),
      ensure_out_unknowns=False,
      ensure_out_inst=False,
      saveable=lambda *_, **__: False)
  if not any(out_used):
    # Short circuit if there is no need to run the fusible at all.
    if discharged_jaxpr_without_fusible is not jaxpr_without_fusible:
      independent_jaxpr, _, out_used, *_ = pe.partial_eval_jaxpr_custom(
          jaxpr_without_fusible,
          in_unknowns=[True] * len(fusion_eqn.outvars),
          in_inst=[True] * len(fusion_eqn.outvars),
          ensure_out_unknowns=False,
          ensure_out_inst=False,
          saveable=lambda *_, **__: False)
      assert not any(out_used)
    return jax_core.eval_jaxpr(independent_jaxpr, candidate_values)

  # Construct fusions for non-constant inputs to the fusible.
  in_fusions_flat = [
      construct_input_fusion(
          candidate_values,
          jaxpr.replace(
              eqns=jaxpr.eqns[:fusion_eqn_index],
          ),
          var,
      )
      for var in fusion_eqn.invars[fusion_eqn.params["num_consts"] :]
  ]
  in_fusions = tree_util.tree_unflatten(
      fusion_eqn.params["in_tree"], in_fusions_flat
  )
  output_fusions, output_permutation = _construct_output_fusions(
      candidate_values,
      jaxpr,
      out_tree,
      fusion_eqn_index,
      fusion_eqn.outvars,
      fusion_eqn.params["out_tree"],
      fusion_eqn.params["output_fusion_prefix"],
      strict_mode=strict_mode,
  )
  out = fusion_eqn.params["func"](*in_fusions, output_fusions)
  flat_out = jax.tree.leaves(out)
  permuted_out = [flat_out[i] for i in output_permutation]
  assert len(permuted_out) == len(jaxpr.outvars), (
      len(permuted_out),
      len(jaxpr.outvars),
  )
  return permuted_out

