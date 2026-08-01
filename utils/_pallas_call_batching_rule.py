
def _pallas_call_batching_rule(
    axis_data,
    args,
    dims,
    *,
    jaxpr: jax_core.Jaxpr,
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    input_output_aliases: tuple[tuple[int, int], ...],
    debug: bool,
    interpret: Any,
    compiler_params: CompilerParams | None,
    cost_estimate: CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: FrozenDict[str, str] | None = None,
    name: str | None = None,
):
  if all(bdim is None for bdim in dims):
    out = pallas_call_p.bind(
        *args,
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
    return out, (None,) * len(out)

  if mesh is not None:
    raise NotImplementedError(
        "pallas_call with a mesh does not support batching"
    )

  def _maybe_squeeze_out_bdim(x: jax_typing.Array, bdim: int | batching.NotMapped
                              ) -> jax_typing.Array:
    return x if bdim is None else jnp.squeeze(x, axis=bdim)

  # this is the _global_ axis size if axis_data.explicit_mesh_axis is not None
  # we want to convert it to the local axis size
  axis_size = axis_data.size
  ema = axis_data.explicit_mesh_axis
  abs_mesh = get_abstract_mesh()
  if ema:
    mesh_size = math.prod(abs_mesh.shape[i] for i in ema)
    axis_size, ragged = divmod(axis_size, mesh_size)
    assert not ragged

  if axis_size == 1:
    # Why are we even vmapping?
    manual_out_avals = [
        o.update(sharding=o.sharding.update(mesh=_as_manual_mesh(o.sharding.mesh, ema)))  # pyrefly: ignore[missing-attribute]
        for o in out_avals] if ema else out_avals
    def temp_f(*args):
      args = map(_maybe_squeeze_out_bdim, args, dims)
      out = pallas_call_p.bind(
          *args,
          jaxpr=jaxpr,
          grid_mapping=grid_mapping,
          mesh=mesh,
          input_output_aliases=input_output_aliases,
          debug=debug,
          interpret=interpret,
          compiler_params=compiler_params,
          cost_estimate=cost_estimate,
          out_avals=tuple(manual_out_avals),
          metadata=metadata,
          name=name,
      )
      return [jnp.expand_dims(x, 0) for x in out]
    if ema:
      with jax_core.remove_explicit_mesh_axis_names(ema):
        temp_f = shard_map(temp_f, out_specs=P(ema), axis_names=set(ema))
    out = temp_f(*args)
    return out, (0,) * len(out)

  # The first num_dynamic_grid_bounds arguments are size-1 arrays that store
  # the size of the dynamic bounds.
  dynamic_grid_args, args = split_list(
      args, [grid_mapping.num_dynamic_grid_bounds]
  )
  dynamic_grid_dims, dims = split_list(
      dims, [grid_mapping.num_dynamic_grid_bounds]
  )
  if all(
      bdim is None or arg.shape[bdim] == 1
      for arg, bdim in zip(dynamic_grid_args, dynamic_grid_dims)
  ):
    dynamic_grid_args = safe_map(
        _maybe_squeeze_out_bdim, dynamic_grid_args, dynamic_grid_dims
    )
  elif any(bdim is not None for bdim in dynamic_grid_dims):
    # TODO(amagni, sharadmv): Explore possibility of batching dynamic grid
    # bounds.
    if ema:
      raise NotImplementedError()
    return _batch_with_explicit_loop(
        args=dynamic_grid_args + args,
        dims=dynamic_grid_dims + dims,
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
  else:
    pass  # No dynamic grid dimensions
  del dynamic_grid_dims
  if grid_mapping.num_index_operands:
    scalar_args, args = split_list(args, [grid_mapping.num_index_operands])
    scalar_bdims, bdims = split_list(dims, [grid_mapping.num_index_operands])
    # Ordinarily, adding support for scalar prefetch in vmap would involve
    # modifying the block specs in a nontrivial way. However, if we are only
    # vmapping over 1-sized dimensions, we can just get rid of the dimensions
    # and pretend we were never vmapped over them at all.
    if all(
        bdim is None or arg.shape[bdim] == 1
        for arg, bdim in zip(scalar_args, scalar_bdims)
    ):
      scalar_args = safe_map(_maybe_squeeze_out_bdim, scalar_args, scalar_bdims)
      scalar_bdims = [None] * len(scalar_args)
      args = (*scalar_args, *args)
      dims = (*scalar_bdims, *bdims)
    else:
      # TODO(amagni,sharadmv,apaszke): enable efficient batching over
      # prefetched scalar args.
      if ema:
        raise NotImplementedError()
      return _batch_with_explicit_loop(
          args=scalar_args + args,
          dims=scalar_bdims + bdims,
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

  if not dims:
    raise NotImplementedError("vmapping pallas_call with no arguments.")
  block_mappings = grid_mapping.block_mappings
  avals = [v.aval for v in jaxpr.invars]
  # How should we pick output dimensions? This actually matters because XLA
  # can't optimize our pallas kernels, and this layout impacts performance. For
  # now, because `vmap` doesn't really offer a way of inferring good output
  # dimensions. For now, we just use 0.
  # TODO(sharadmv): explore inferring better output dimensions via a heuristic
  # TODO(sharadmv): explore a long term solution to output dim inference

  args, dims = _broadcast_input_output_aliases(
      args, dims, input_output_aliases=input_output_aliases, axis_size=axis_size
  )

  all_dims = list(dims) + [0] * grid_mapping.num_outputs
  num_index_operands = grid_mapping.num_index_operands
  num_scratch_operands = grid_mapping.num_scratch_operands

  # Only add a batch dimension for the avals that actually have a grid mapping.
  # This excludes scalar prefetch inputs (the first in the list) and scratch
  # operands (the last in the list).
  avals_to_batch = avals[num_index_operands:(len(avals) - num_scratch_operands)]

  batched_block_mappings = map(
      partial(
          _batch_block_mapping,
          grid_mapping,
          axis_size,
      ),
      avals_to_batch,
      all_dims[num_index_operands:],
      block_mappings,
  )

  index_map_tree_args, index_map_tree_kwargs = grid_mapping.index_map_tree.unflatten(
      grid_mapping.index_map_avals)
  assert not index_map_tree_kwargs
  batched_index_map_args = (pallas_core.index_map_grid_aval,) + index_map_tree_args
  batched_index_map_avals, batched_index_map_tree = tree_util.tree_flatten(
      (batched_index_map_args, {}))

  axis_size_is_dynamic = not jax_core.is_constant_dim(axis_size)
  new_grid_dim = pallas_core.dynamic_grid_dim if axis_size_is_dynamic else axis_size

  batched_grid_mapping = grid_mapping.replace(
      grid=(new_grid_dim, *grid_mapping.grid),
      block_mappings=tuple(batched_block_mappings),
      index_map_avals=tuple(batched_index_map_avals),
      index_map_tree=batched_index_map_tree,
      num_index_operands=num_index_operands,
      vmapped_dims=(0,) + tuple(a + 1 for a in grid_mapping.vmapped_dims),
  )

  # Avoid scaling the cost estimate by the batch size if the batch size is a
  # dynamic shape (DimExpr).
  # https://docs.jax.dev/en/latest/export/shape_poly.html#computing-with-dimension-variables
  if cost_estimate is not None and not axis_size_is_dynamic:
    batched_cost_estimate = CostEstimate(
        flops=cost_estimate.flops * axis_size,
        bytes_accessed=cost_estimate.bytes_accessed * axis_size,
        transcendentals=cost_estimate.transcendentals * axis_size,
    )
  else:
    batched_cost_estimate = None

  assert all(isinstance(aval, jax_core.ShapedArray) for aval in out_avals)

  batched_out_avals = []
  for aval in out_avals:
    assert isinstance(aval, jax_core.ShapedArray)
    manual_mesh = (_as_manual_mesh(aval.sharding.mesh, ema) if ema else
                   aval.sharding.mesh)
    sharding = aval.sharding.update(
        mesh=manual_mesh, spec=tuple_insert(aval.sharding.spec, 0, None))
    shape = tuple_insert(aval.shape, 0, axis_size)
    batched_out_avals.append(aval.update(shape=shape, sharding=sharding))
  batched_out_avals = tuple(batched_out_avals)

  bind = partial(
      pallas_call_p.bind,
      jaxpr=jaxpr,
      grid_mapping=batched_grid_mapping,
      mesh=mesh,
      input_output_aliases=input_output_aliases,
      debug=debug,
      interpret=interpret,
      compiler_params=compiler_params,
      cost_estimate=batched_cost_estimate,
      out_avals=batched_out_avals,
      metadata=metadata,
      name=name,
  )

  if ema:
    # TODO all batching rules should probably be in outer mesh ctx
    with jax_core.remove_explicit_mesh_axis_names(ema):
      bind = shard_map(bind, out_specs=P(ema), axis_names=set(ema))

  if axis_size_is_dynamic:
    dynamic_grid_args = [axis_size, *dynamic_grid_args]
  out = bind(*dynamic_grid_args, *args)
  return out, (0,) * len(out)

