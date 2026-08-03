from typing import Any

def get_grid_mapping(
    grid_spec: GridSpec,
    in_avals: Sequence[jax_core.AbstractValue],
    in_tree: tree_util.PyTreeDef,
    in_origins: Sequence[OriginStr],
    out_avals: Sequence[jax_core.AbstractValue],
    out_tree: tree_util.PyTreeDef,
    out_origins: Sequence[OriginStr],
    allow_captured_consts: bool = False,
    debug: bool = False,
) -> tuple[tuple[jax_core.AbstractValue, ...], GridMapping]:
  if dynamic_shapes_export_enabled():
    dim_check: Any = jax_core.is_dim
  else:
    dim_check: Any = jax_core.is_constant_dim
  assert all(i is None or dim_check(i) for i in grid_spec.grid)
  grid_mapping_grid: GridMappingGrid = tuple(  # pyrefly: ignore[bad-assignment]
      dynamic_grid_dim if (  # pyrefly: ignore[bad-argument-type]
          d is None or (not jax_core.is_constant_dim(d) and not dynamic_shapes_export_enabled())
      ) else d
      for d in grid_spec.grid
  )
  # The inputs for the index maps
  index_map_avals = (
      index_map_grid_aval.update(sharding=jax_core.get_cur_mesh_sharding()),
  ) * len(grid_spec.grid)
  index_map_tree = tree_util.tree_structure((index_map_avals, {}))

  num_scalar_prefetch: int = getattr(grid_spec, "num_scalar_prefetch", 0)
  if num_scalar_prefetch:
    all_avals = tree_util.tree_unflatten(in_tree, in_avals)
    scalar_avals, unflat_in_avals = split_list(
        all_avals, [num_scalar_prefetch])
    flat_scalar_avals, scalar_tree = tree_util.tree_flatten(scalar_avals)
    num_flat_scalar_prefetch = len(flat_scalar_avals)
    scalar_ref_avals = [
        grid_spec._make_scalar_ref_aval(aval)
        for aval in flat_scalar_avals]
    jaxpr_scalar_ref_avals = tree_util.tree_unflatten(
        scalar_tree, scalar_ref_avals)
    in_avals, in_tree = tree_util.tree_flatten(tuple(unflat_in_avals))
    index_map_tree = tree_util.tree_structure(((*index_map_avals,
                                                *scalar_avals), {}))
    index_map_avals = (*index_map_avals, *scalar_ref_avals)
    del scalar_ref_avals, flat_scalar_avals, scalar_tree
    del scalar_avals, unflat_in_avals, all_avals
  else:
    num_flat_scalar_prefetch = 0
    jaxpr_scalar_ref_avals = ()
  if grid_spec.scratch_shapes:
    flat_scratch_shapes, scratch_tree = tree_util.tree_flatten(
        grid_spec.scratch_shapes)
    flat_scratch_avals = tuple(s.get_ref_aval() for s in flat_scratch_shapes)
    jaxpr_scratch_avals = tree_util.tree_unflatten(
        scratch_tree, flat_scratch_avals)
    if not isinstance(jaxpr_scratch_avals, (tuple, list)):
      jaxpr_scratch_avals = (jaxpr_scratch_avals,)
    del flat_scratch_shapes, scratch_tree
  else:
    flat_scratch_avals = ()
    jaxpr_scratch_avals = ()

  def _with_default_memory_space(bs: BlockSpec):
    if bs is no_block_spec:
      return BlockSpec(memory_space=MemorySpace.DEFAULT)
    elif bs.memory_space is None:
      return bs.replace(memory_space=MemorySpace.DEFAULT)
    else:
      return bs

  if grid_spec.in_specs is not no_block_spec:
    flat_in_specs, in_specs_tree = tree_util.tree_flatten(grid_spec.in_specs)
    if in_specs_tree != in_tree:
      raise ValueError(
          pytreedef_mismatch_err_msg("`in_specs`", in_specs_tree,
                                     "`inputs`", in_tree))
    flat_in_specs = [_with_default_memory_space(bs) for bs in flat_in_specs]
  else:
    flat_in_specs = (
        [BlockSpec(memory_space=MemorySpace.DEFAULT)] * len(in_avals))

  in_block_mappings = map(
      partial(
          _convert_block_spec_to_block_mapping,
          index_map_avals=index_map_avals,
          index_map_tree=index_map_tree,
          grid=grid_mapping_grid,
          vmapped_dims=(),
          allow_captured_consts=allow_captured_consts,
          debug=debug,
      ),
      flat_in_specs,
      in_origins[num_flat_scalar_prefetch:],
      in_avals,
  )

  if grid_spec.out_specs is not no_block_spec:
    flat_out_specs, out_specs_tree = tree_util.tree_flatten(grid_spec.out_specs)
    if out_specs_tree != out_tree:
      raise ValueError(
          pytreedef_mismatch_err_msg("`out_specs`", out_specs_tree,
                                     "`out_shape`", out_tree))
    flat_out_specs = [_with_default_memory_space(bs) for bs in flat_out_specs]
  else:
    flat_out_specs = (
        [BlockSpec(memory_space=MemorySpace.DEFAULT)] * len(out_avals))

  out_block_mappings = map(
      partial(
          _convert_block_spec_to_block_mapping,
          index_map_avals=index_map_avals,
          index_map_tree=index_map_tree,
          grid=grid_mapping_grid,
          vmapped_dims=(),
          allow_captured_consts=allow_captured_consts,
          debug=debug,
      ),
      flat_out_specs,
      out_origins,
      out_avals,
  )
  grid_mapping = GridMapping(
      grid=grid_mapping_grid,
      grid_names=grid_spec.grid_names,
      block_mappings=(*in_block_mappings, *out_block_mappings),
      index_map_avals=index_map_avals,
      index_map_tree=index_map_tree,
      vmapped_dims=(),
      num_index_operands=num_flat_scalar_prefetch,
      num_inputs=len(flat_in_specs),
      num_outputs=len(flat_out_specs),
      scratch_avals=flat_scratch_avals,
      debug=debug,
  )
  grid_mapping.check_invariants()
  in_ref_avals = [bm.ref_aval for bm in in_block_mappings]
  jaxpr_in_ref_avals = tree_util.tree_unflatten(in_tree, in_ref_avals)
  jaxpr_in_avals = (*jaxpr_scalar_ref_avals,
                    *jaxpr_in_ref_avals)
  out_ref_avals = [bm.ref_aval for bm in out_block_mappings]
  jaxpr_out_avals = tree_util.tree_unflatten(out_tree, out_ref_avals)
  if not isinstance(jaxpr_out_avals, (tuple, list)):
    jaxpr_out_avals = (jaxpr_out_avals,)
  return (*jaxpr_in_avals, *jaxpr_out_avals,
          *jaxpr_scratch_avals), grid_mapping

