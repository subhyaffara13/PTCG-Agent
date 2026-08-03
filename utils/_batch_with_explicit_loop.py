from typing import Any

def _batch_with_explicit_loop(
    args: Sequence[jax_typing.Array],
    dims: Sequence[int | batching.NotMapped],
    *,
    jaxpr: jax_core.Jaxpr,
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    input_output_aliases: tuple[tuple[int, int], ...],
    debug: bool,
    interpret: Any,
    compiler_params: Any,
    cost_estimate: CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: FrozenDict[str, str] | None,
    name: str | None,
):
  """Batch the pallas_call by calling it in loop over the batch size.

  This function provides a fallback implementation of batching a pallas_call
  for the cases in which adding a batch dimension to the pallas grid is not
  supported. This is currently the case when the batched dimension corresponds
  to a dynamic axis or a scalar prefetch argument.

  This implementation builds a HLO loop that dynamic_slices the inputs according
  to the current iteration index and dynamic_updates an (initially empty) output
  allocation.
  """
  if not dims:
    raise NotImplementedError("vmapping pallas_call with no arguments.")

  (axis_size,) = {
      arg.shape[dim]
      for arg, dim in zip(args, dims)
      if dim is not None
  }

  args, dims = _broadcast_input_output_aliases(
      args,
      dims,
      input_output_aliases=input_output_aliases,
      axis_size=axis_size,
  )

  # The output arrays are completely overwritten, so we can just initialize
  # empty arrays.
  initial_state = [
      jnp.empty(tuple_insert(bm.array_aval.shape, 0, axis_size),
                dtype=bm.array_aval.dtype)
      for bm in grid_mapping.block_mappings_output
  ]

  def body(batch_index: jax_typing.Array, state: list[jax_typing.Array]) -> list[jax_typing.Array]:

    batch_args = []

    for arg, dim in zip(args, dims):
      # If the argument is mapped, extract a slice of size 1 in the mapped
      # dimension at the current index.
      if dim is None:
        batch_args.append(arg)
      else:
        batch_args.append(
            jnp.squeeze(
                lax.dynamic_slice_in_dim(
                    operand=arg,
                    start_index=batch_index,
                    slice_size=1,
                    axis=dim,
                ),
                axis=dim,
            )
        )
    batch_out = pallas_call_p.bind(
        *batch_args,
        jaxpr=jaxpr,
        grid_mapping=grid_mapping,
        mesh=mesh,
        input_output_aliases=input_output_aliases,
        debug=debug,
        interpret=interpret,
        compiler_params=compiler_params,
        cost_estimate=cost_estimate,
        out_avals=out_avals,
        metadata=metadata,
        name=name,
    )
    for i, batch_out_array in enumerate(batch_out):
      state[i] = lax.dynamic_update_index_in_dim(
          state[i],
          batch_out_array,
          batch_index,
          axis=0,
      )

    return state

  result = lax.fori_loop(0, axis_size, body, initial_state, unroll=False)

  return result, (0,) * len(result)

