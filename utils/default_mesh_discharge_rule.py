
def default_mesh_discharge_rule(
    in_avals,
    out_avals,
    *args,
    mesh,
    compiler_params,
    jaxpr,
    debug,
    interpret,
    cost_estimate,
    name,
    metadata,
):
  """Discharges a ``core_map`` over a mesh to a ``mpmd_map``."""
  if not all(
      isinstance(aval, state.AbstractRef) for aval in (in_avals + out_avals)
  ):
    raise ValueError(
        "default_mesh_discharge_rule only supports Ref inputs/outputs."
    )

  input_idx = {v: i for i, v in enumerate((*jaxpr.constvars, *jaxpr.invars))}
  modified_idxs = sorted(
      input_idx[eff.input]
      for eff in jaxpr.effects
      if isinstance(eff, state_types.WriteEffect)
      and input_idx[eff.input] < len(in_avals)
  )
  default_memory_space = mesh.default_memory_space
  in_memory_spaces = [get_memory_space_aval(aval) for aval in in_avals]
  in_memory_spaces = [
      default_memory_space if m is None else m for m in in_memory_spaces
  ]
  args = [
      with_memory_space_constraint_p.bind(arg, memory_space=memory_space)
      if memory_space is not default_memory_space else arg
      for arg, memory_space in zip(args, in_memory_spaces)
  ]

  scratch_avals = [v.aval for v in jaxpr.invars]
  scratch_types = tuple(
      MemoryRef(v.inner_aval, v.memory_space) for v in scratch_avals
  )

  def body(*args):
    # Due to aliasing, ``args`` contains aliased inputs and outputs so we
    # remove outputs.
    in_refs, _, scratch_refs = split_list(
        args, [len(in_avals), len(modified_idxs)]
    )
    jax_core.eval_jaxpr(jaxpr, in_refs, *scratch_refs)

  from jax._src.pallas import mpmd  # Avoid circular dependency.

  outs = mpmd._mpmd_map(
      [(mesh, body)],
      out_types=tuple(_get_sds(in_avals[idx]) for idx in modified_idxs),
      input_output_aliases={
          in_idx: out_idx for out_idx, in_idx in enumerate(modified_idxs)
      },
      scratch_types=scratch_types,
      compiler_params=compiler_params,
      interpret=interpret,
      debug=debug,
      cost_estimate=cost_estimate,
      metadata=metadata,
      name=name,
  )(*args)

  # ``outs`` lacks the unmodified inputs. Add them back in.
  all_outs = [None] * len(args)  # pyrefly: ignore[unsupported-assignment]
  for out_idx, in_idx in enumerate(modified_idxs):
    all_outs[in_idx] = outs[out_idx]
  return all_outs, ()

