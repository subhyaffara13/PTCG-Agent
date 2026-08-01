
def _pipeline_body_lowering_rule(ctx, *args_flat, jaxpr, in_tree, **_):
  # TODO(rdyro): This function is a near duplicate of _jaxpr_call_lowering_rule
  # from sc_lowering.py, we should factor out and unify the two.
  (indices, body_consts, refs) = in_tree.unflatten(args_flat)
  (_, body_const_shapes, refs_shapes) = in_tree.unflatten(ctx.block_shapes)

  refs_avals = tuple(var.aval for var in jaxpr.invars)
  # manually resolve the transformed refs
  if refs:
    resolved_refs, resolved_ref_shapes = zip(
        *(_transform_ref(ref, ref_aval, ref_shape)
          for ref, ref_aval, ref_shape in zip(refs, refs_avals, refs_shapes)))
  else:
    resolved_refs, resolved_ref_shapes = (), ()

  user_grid_indices = ctx.lowering_context.user_grid_indices
  # TODO(rdyro): As a temporary workaround, to support both core mesh axes
  # (jax.lax.axis_(index|size)) and memory pipeline axes
  # (pl.(program_id|num_programs)), we append the core grid to the end of the
  # end of the user grid dimensions. This is error prone (the user could request
  # a core grid dimension with pl.program_id); we should fix this soon.
  lowering_context = ctx.lowering_context.replace(
      user_grid_indices=(tuple(indices)
                         + tuple(user_grid_indices[len(indices):])),
      block_shapes=(list(body_const_shapes)
                    + list(resolved_ref_shapes))
  )
  # Lift the constants out of the jaxpr, disabling checks to avoid a redundant
  # re-checking of jaxpr, like its grid and sharding information.
  with config.enable_checks(False):
    jaxpr = pe.convert_constvars_jaxpr(jaxpr)
  assert len(jaxpr.invars) == len(lowering_context.block_shapes)
  return jaxpr_subcomp(lowering_context, jaxpr, *body_consts, *resolved_refs)

