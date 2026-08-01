
def _construct_output_fusions(
    candidate_values,
    jaxpr,
    out_tree,
    fusion_eqn_index,
    fusion_eqn_outvars,  # Flat list of vars output by the fusible eqn
    fusion_eqn_out_tree,  # Tree structure of the fusible eqn outputs
    output_fusion_prefix,  # Pytree defining output groups
    *,
    strict_mode: bool = True,
):
  # 1. Create jaxpr_out: represents computation *after* the fusible
  #    Inputs: fusion_eqn_outvars
  #    Outputs: jaxpr.outvars
  jaxpr_out, all_values, _, _, _ = _construct_fusion_jaxpr(
      candidate_values,
      jaxpr.replace(
          eqns=jaxpr.eqns[:fusion_eqn_index]
          + jaxpr.eqns[fusion_eqn_index + 1 :]
      ),
      tree_util.tree_unflatten(out_tree, jaxpr.outvars),  # Original outputs
      tree_util.tree_unflatten(
          fusion_eqn_out_tree, fusion_eqn_outvars
      ),  # Fusible outputs as inputs
  )

  # 2. Group fusible outputs based on the mask
  unflat_fusible_outvars = jax.tree.unflatten(
      fusion_eqn_out_tree, fusion_eqn_outvars
  )
  partial_flat = jax.tree.structure(output_fusion_prefix).flatten_up_to(
      unflat_fusible_outvars
  )
  if len(partial_flat) > 1:
    if any(isinstance(e, (state_types.WriteEffect, state_types.AccumEffect))
           for e in jaxpr_out.effects):
      raise ValueError("Multiple output fusions are not currently supported "
                       "for fusions that write to Refs.")

  # 3. Calculate dependencies and check disjointedness
  downstream_outputs_used_masks = []  # List of bool tuples, one per group
  already_used_final_outputs = set()  # Indices of final outputs already claimed
  for outvars_group in partial_flat:
    # Identify vars in this group
    used_fusible_outvars = set(jax.tree.leaves(outvars_group))
    # Create mask for jaxpr_out inputs corresponding to this group
    in_used_mask = [
        True if v in used_fusible_outvars else False for v in jaxpr_out.invars
    ]
    # Trace dependencies through jaxpr_out to find which final outputs are affected
    downstream_used_mask = _find_downstream(
        jaxpr_out, in_used_mask
    )  # Mask for jaxpr_out.outvars (== jaxpr.outvars)

    # Check for overlap in final output usage across groups
    for i, used in enumerate(downstream_used_mask):
      if used:
        if i in already_used_final_outputs:
          raise ValueError(
              "Outputs must be disjoint in order to use separate output fusions"
          )
        already_used_final_outputs.add(i)
    downstream_outputs_used_masks.append(downstream_used_mask)

  for u in list(zip(*downstream_outputs_used_masks))[len(jaxpr_out.outvars):]:
    if sum(u) == 0:
      raise ValueError("A write to a Ref in a fusion must depend on "
                       "an output of the fusible")
  downstream_outputs_used_masks = [
      used[:len(jaxpr_out.outvars)] for used in downstream_outputs_used_masks]

  # 4. Construct output permutation needed to restore original output order
  output_permutation = _construct_output_permutation(
      downstream_outputs_used_masks
  )

  # Construct fusions for each group by DCEing the jaxpr_out
  output_fusions: list[fusion_lib.Fusion | None] = []
  for i, outvars_group in enumerate(partial_flat):
    flat_group_vars, _ = tree_util.tree_flatten(outvars_group)
    downstream_used_mask = downstream_outputs_used_masks[i]

    used_jaxpr_invars = [False] * len(all_values) + [
        v in flat_group_vars for v in jaxpr_out.invars
    ]
    jaxpr_out_for_group, used_consts, _ = pe.dce_jaxpr_consts(
        jaxpr_out, downstream_used_mask, instantiate=used_jaxpr_invars
    )
    values_for_jaxpr = tuple(
        c for used, c in zip(used_consts, all_values, strict=True) if used
    )

    if (
        not jaxpr_out_for_group.eqns
        and jaxpr_out_for_group.outvars == jaxpr_out_for_group.invars
    ):
      output_fusions.append(None)
      continue

    def _fn(jaxpr, vals, *args, **kwargs):
      flat_args, _ = tree_util.tree_flatten((args, kwargs))
      out_flat = jax_core.eval_jaxpr(jaxpr, vals, *flat_args)
      return tuple(out_flat)

    fn = functools.partial(_fn, jaxpr_out_for_group, values_for_jaxpr)
    in_type = jax.tree.map(lambda x: x.aval, outvars_group)
    out_type = tuple(v.aval for v in jaxpr_out_for_group.outvars)
    fusion = fusion_lib.Fusion(
        fn,
        (in_type, {}),
        out_type,
        strict_mode=strict_mode,
    )
    output_fusions.append(fusion)

  return (
      tree_util.tree_unflatten(
          tree_util.tree_structure(output_fusion_prefix), output_fusions
      ),
      output_permutation,
  )

