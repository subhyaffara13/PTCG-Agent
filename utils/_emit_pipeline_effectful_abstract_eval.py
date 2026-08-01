
def _emit_pipeline_effectful_abstract_eval(
    *avals, body_jaxpr: core.Jaxpr, body_consts_len,
    grid_mapping, _num_extra_dynamic, args_tree, **params):
  del params
  index_map_consts_counts = tuple(
      len(bm.index_map_jaxpr.consts) for bm in grid_mapping.block_mappings)
  num_index_map_consts = sum(index_map_consts_counts)
  num_dynamic = grid_mapping.num_dynamic_grid_bounds + _num_extra_dynamic
  offset = num_index_map_consts + num_dynamic + body_consts_len

  # Because we can have TransformedRefs as argumetns to the body, but the flat
  # arguments are flattened Refs and transforms, we unflatten the positional
  # indices to be able to identify the index of an n-th Ref from a positional
  # index.
  indices_flat = list(range(offset, len(avals)))
  flat_refs_idx, _ = tracing_registry.flatten(
      args_tree.unflatten(indices_flat), is_transformed_ref)
  # Helper to resolve the underlying AbstractRef index in `avals` for any leaf.
  get_ref_idx = lambda x: x.ref if isinstance(x, state.TransformedRef) else x

  out_effects: set[effects.Effect] = set()
  num_inputs = grid_mapping.num_inputs
  # Attach base ReadEffect / WriteEffect instances for the logical references.
  for i, x in enumerate(flat_refs_idx):
    ref_idx = get_ref_idx(x)
    if isinstance(avals[ref_idx], state.AbstractRef):
      out_effects.add(ReadEffect(ref_idx)
                      if i < num_inputs else WriteEffect(ref_idx))

  # Propagate effects from `body_jaxpr`, mapping them to the correct indices in
  # `avals`.
  body_input_idx = {v: i for i, v in enumerate(
      (*body_jaxpr.constvars, *body_jaxpr.invars))}
  for e in body_jaxpr.effects:
    if not isinstance(e, effects.JaxprInputEffect):
      out_effects.add(e)
      continue
    input_idx = body_input_idx[e.input]
    if input_idx < len(body_jaxpr.constvars):
      const_offset = num_index_map_consts + num_dynamic
      out_effects.add(e.replace(const_offset + input_idx))
    else:
      invar_idx = input_idx - len(body_jaxpr.constvars)
      if invar_idx < num_inputs and isinstance(e, WriteEffect):
        raise ValueError(
            f"WriteEffect should not apply to an input buffer {invar_idx} in"
            f" pipeline body jaxpr: {body_jaxpr}")
      ref_idx = get_ref_idx(flat_refs_idx[invar_idx])
      out_effects.add(e.replace(ref_idx))
  return (), frozenset(out_effects)

