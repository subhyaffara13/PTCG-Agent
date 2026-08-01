
def _emit_pipeline_lowering_rule(
    ctx, *args, grid_mapping, _num_extra_dynamic, _static_grid_offsets,
    args_tree, body_jaxpr, body_consts_len, **params
):
  index_map_consts_counts = tuple(
      len(bm.index_map_jaxpr.consts) for bm in grid_mapping.block_mappings)

  def wrapped_pipeline_fun(*all_args, grid_mapping=grid_mapping):
    num_index_map_consts = sum(index_map_consts_counts)
    num_dynamic = grid_mapping.num_dynamic_grid_bounds + _num_extra_dynamic
    grid_mapping_consts, dynamic_vals, body_consts, flat_refs = (
        jax_util.split_list(
            all_args, [num_index_map_consts, num_dynamic, body_consts_len]))

    index_map_consts = jax_util.split_list(
        grid_mapping_consts, index_map_consts_counts)
    new_bms = []
    for i, bm in enumerate(grid_mapping.block_mappings):
      bm = bm.replace(index_map_jaxpr=core.ClosedJaxpr(
          bm.index_map_jaxpr.jaxpr, index_map_consts[i]))
      new_bms.append(bm)
    grid_mapping = dataclasses.replace(grid_mapping, block_mappings=new_bms)

    flat_refs, _ = tracing_registry.flatten(  # flatten to TransformedRefs
        args_tree.unflatten(flat_refs), is_transformed_ref)
    dynamic_vals_iter = iter(dynamic_vals)
    grid = tuple(next(dynamic_vals_iter)
                 if pallas_core.is_dynamic_dim(d) else d
                 for d in grid_mapping.grid)
    grid_offsets = tuple(next(dynamic_vals_iter)
                         if pallas_core.is_dynamic_dim(d) else d
                         for d in _static_grid_offsets)
    in_specs = [
        bm.to_block_spec()
        for bm in grid_mapping.block_mappings[:grid_mapping.num_inputs]]
    out_specs = [
        bm.to_block_spec()
        for bm in grid_mapping.block_mappings[grid_mapping.num_inputs:]]

    def new_body(indices, *args):
      original_indices = tuple(
          idx for i, idx in enumerate(indices)
          if i not in grid_mapping.vmapped_dims
      )
      indices_consts_args = (original_indices, body_consts, args)
      args_flat, args_tree = tracing_registry.flatten(indices_consts_args)
      return pipeline_body_p.bind(
          *args_flat,
          jaxpr=body_jaxpr,
          in_tree=args_tree,
          num_inputs=grid_mapping.num_inputs,
      )

    pipeline_fun = _emit_pipeline(
        new_body, grid=grid, in_specs=in_specs, out_specs=out_specs,
        _grid_offsets=grid_offsets, _explicit_indices=True, **params)

    # Use a logical grid env (excluding vmapped dims) so that
    # num_programs(axis) resolves against the user's original grid axes.
    pipeline_grid = tuple(d for i, d in enumerate(grid_mapping.grid)
                          if i not in grid_mapping.vmapped_dims)

    # re-create the pallas core grid env
    grid_names = ctx.lowering_context.grid_names
    grid_sizes = ctx.lowering_context.grid_sizes
    if grid_names is None:
      grid_names = (None,) * len(grid_sizes)
    axis_env_ctx = core.extend_axis_env_nd(
        [(name, size) for name, size in zip(grid_names, grid_sizes)
        if name is not None and isinstance(size, int)]
    )

    # run the actual pipeline function
    with (axis_env_ctx, pallas_core.tracing_grid_env(pipeline_grid, ())):
      pipeline_fun(*flat_refs)
    return ()

  dbg = api_util.debug_info(
      "emit_pipeline_lowering", wrapped_pipeline_fun, ctx.avals_in, {})
  wrapped_lu_fun = lu.wrap_init(wrapped_pipeline_fun, debug_info=dbg)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_lu_fun, ctx.avals_in)
  assert not consts and not jaxpr.constvars, (
      f"wrapped_pipeline_fun should not close over JAX constants, but found: "
      f"{consts=} {jaxpr.constvars=}")
  jaxpr = pe.convert_constvars_jaxpr(jaxpr)
  num_index_map_consts = sum(index_map_consts_counts)
  num_dynamic = grid_mapping.num_dynamic_grid_bounds + _num_extra_dynamic
  _, dynamic_vals, _, _ = jax_util.split_list(
      args, [num_index_map_consts, num_dynamic, body_consts_len]
  )
  grid_val_iter = iter(dynamic_vals)
  grid = tuple(next(grid_val_iter) if pallas_core.is_dynamic_dim(d)
               else ir_constant(d) for d in grid_mapping.grid)

  # TODO(rdyro): We append the core grid dimensions to the end of the memory
  # pipeline grid dimensions as a temporary workaround, but this conflates the
  # pipeline and core grid.  Separate them in the lowering definition.
  grid_names = ctx.lowering_context.grid_names
  if grid_names is None:
    grid_names = (None,) * len(ctx.lowering_context.grid_sizes)
  grid_names = (tuple(None for i, _ in enumerate(grid)
                      if i not in grid_mapping.vmapped_dims)
                + (tuple(grid_names or ())))
  user_grid_indices = (tuple(g for i, g in enumerate(grid)
                             if i not in grid_mapping.vmapped_dims)
                       + tuple(ctx.lowering_context.user_grid_indices))
  grid += tuple(ctx.lowering_context.grid_sizes)

  lowering_context = ctx.lowering_context.replace(
      block_shapes=ctx.block_shapes,
      grid_sizes=grid,
      grid_names=grid_names,
      user_grid_indices=user_grid_indices,
      vmapped_dims=grid_mapping.vmapped_dims,
  )

  assert len(jaxpr.invars) == len(lowering_context.block_shapes)
  valid_grid_sizes = tuple(d for i, d in enumerate(lowering_context.grid_sizes)
                         if i not in grid_mapping.vmapped_dims)
  assert len(valid_grid_sizes) == len(lowering_context.grid_names)
  return jaxpr_subcomp(lowering_context, jaxpr, *args)

