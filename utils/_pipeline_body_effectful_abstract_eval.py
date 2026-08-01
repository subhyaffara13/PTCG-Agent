
def _pipeline_body_effectful_abstract_eval(
    *avals, jaxpr, in_tree, num_inputs, **params
):
  del params
  # Because `avals` are grid indices, body constants, and flattened
  # TransformedRefs as arguments, we unflatten a flat index list to be able to
  # identify the index of an n-th Ref from a positional index.
  indices_flat = list(range(len(avals)))
  (_, consts_idx, refs_idx) = in_tree.unflatten(indices_flat)
  flat_refs_idx, _ = tracing_registry.flatten(refs_idx, is_transformed_ref)
  flat_consts_idx, _ = tracing_registry.flatten(consts_idx)
  # Helper to resolve the underlying AbstractRef index in `avals` for any leaf.
  get_ref_idx = lambda x: x.ref if isinstance(x, state.TransformedRef) else x

  out_effects: set[effects.Effect] = set()
  # Attach base ReadEffect / WriteEffect instances for the logical references.
  for i, x in enumerate(flat_refs_idx):
    ref_idx = get_ref_idx(x)
    if isinstance(avals[ref_idx], state.AbstractRef):
      out_effects.add(ReadEffect(ref_idx) if i < num_inputs else WriteEffect(ref_idx))
  # Propagate effects from `jaxpr`, mapping them to the correct indices in `avals`.
  jaxpr_input_idx = {v: i for i, v in enumerate(
      (*jaxpr.constvars, *jaxpr.invars))}
  for e in jaxpr.effects:
    if not isinstance(e, effects.JaxprInputEffect):
      out_effects.add(e)
      continue
    input_idx = jaxpr_input_idx[e.input]
    if input_idx < len(jaxpr.constvars):
      out_effects.add(e.replace(flat_consts_idx[input_idx]))
    else:
      invar_idx = input_idx - len(jaxpr.constvars)
      if invar_idx < num_inputs and isinstance(e, WriteEffect):
        raise ValueError(f"WriteEffect on input buffer {invar_idx}")
      ref_idx = get_ref_idx(flat_refs_idx[invar_idx])
      out_effects.add(e.replace(ref_idx))
  return (), frozenset(out_effects)

