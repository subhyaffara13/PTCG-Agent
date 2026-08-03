from typing import Any

def _pallas_call_state_discharge_rule(
    avals_in,
    avals_out,
    *args,
    jaxpr: jax_core.Jaxpr,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    debug: bool,
    interpret: Any,
    compiler_params: CompilerParams | None,
    cost_estimate: CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: FrozenDict[str, str] | None,
    name: str | None,
):
  del avals_out
  assert all(isinstance(v.aval, state.AbstractRef) for v in jaxpr.constvars)
  num_refs = len(jaxpr.constvars)
  ref_avals, rest_in_avals = split_list(avals_in, [num_refs])
  assert all(isinstance(ref_aval, state.AbstractRef) for ref_aval in ref_avals)
  ref_avals = [
      state.AbstractRef(
          ref_aval.inner_aval, pallas_core.MemorySpace.ANY
      )
      for ref_aval in ref_avals
  ]
  ref_block_specs = [
      pallas_core.BlockSpec(memory_space=pallas_core.MemorySpace.ANY)
  ] * num_refs
  ref_block_mappings = [
      block_spec.to_block_mapping(
          origin="",  # TODO(sharadmv): enable origins for refs
          array_aval=cast(jax_core.ShapedArray, ref_aval.inner_aval),
          index_map_avals=grid_mapping.index_map_avals,
          index_map_tree=grid_mapping.index_map_tree,
          grid=grid_mapping.grid,
          vmapped_dims=grid_mapping.vmapped_dims,
          debug=debug,
      )
      for ref_aval, block_spec in zip(ref_avals, ref_block_specs)
  ]
  in_block_mappings, out_block_mappings = split_list(
      grid_mapping.block_mappings, [grid_mapping.num_inputs]
  )
  new_block_mappings = (
      *ref_block_mappings,
      *in_block_mappings,
      *ref_block_mappings,
      *out_block_mappings,
  )
  new_grid_mapping = grid_mapping.replace(
      block_mappings=new_block_mappings,
      num_inputs=grid_mapping.num_inputs + num_refs,
      num_outputs=grid_mapping.num_outputs + num_refs)
  new_input_output_aliases = [
      (i + grid_mapping.num_index_operands, i) for i in range(num_refs)
  ]
  for i, o in input_output_aliases:
    new_input_output_aliases.append((i + num_refs, o + num_refs))
  ref_out_avals = [ref_aval.inner_aval for ref_aval in ref_avals]
  new_out_avals = (*ref_out_avals, *out_avals)
  ref_args, dynamic_grid_bounds, index_operands, rest_args = split_list(
      args,
      [
          num_refs,
          grid_mapping.num_dynamic_grid_bounds,
          grid_mapping.num_index_operands,
      ],
  )
  def _rewritten_body(*args):
    index_args, in_args, out_args, rest_args = split_list(
        args, [new_grid_mapping.num_index_operands, new_grid_mapping.num_inputs,
               new_grid_mapping.num_outputs])
    ref_in_args, in_args = split_list(in_args, [num_refs])
    ref_out_args, out_args = split_list(out_args, [num_refs])
    # We don't care about ref_out_args because they are aliased to ref_in_args
    del ref_out_args
    jax_core.eval_jaxpr(
        jaxpr, ref_in_args, *index_args, *in_args, *out_args, *rest_args
    )
    return []
  index_map_avals, jaxpr_in_avals, jaxpr_out_avals, jaxpr_rest_avals = (
      split_list(
          [v.aval for v in jaxpr.invars],
          [
              grid_mapping.num_index_operands,
              grid_mapping.num_inputs,
              grid_mapping.num_outputs,
          ],
      )
  )
  new_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(_rewritten_body,
                   debug_info=jaxpr.debug_info.with_unknown_names()),
      [
          *index_map_avals,
          *ref_avals,
          *jaxpr_in_avals,
          *ref_avals,
          *jaxpr_out_avals,
          *jaxpr_rest_avals,
      ],
  )
  out_flat = pallas_call_p.bind(
      *consts,
      *dynamic_grid_bounds,
      *index_operands,
      *ref_args,
      *rest_args,
      jaxpr=new_jaxpr,
      input_output_aliases=tuple(new_input_output_aliases),
      grid_mapping=new_grid_mapping,
      mesh=mesh,
      debug=debug,
      interpret=interpret,
      compiler_params=compiler_params,
      cost_estimate=cost_estimate,
      out_avals=new_out_avals,
      metadata=metadata,
      name=name,
  )
  refs_out, rest = split_list(out_flat, [num_refs])
  updated_vals_in = refs_out + [None] * len(rest_in_avals)
  return updated_vals_in, rest

