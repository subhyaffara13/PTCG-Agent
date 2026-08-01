
def _mpmd_map_fallback_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    meshes,
    jaxprs,
    out_avals,
    input_output_aliases,
    compiler_params,
    interpret,
    debug,
    cost_estimate,
    metadata,
    name,
    external_meshes,
):
  if len(jaxprs) != 1:
    raise NotImplementedError(
        "Lowering multiple mesh/function pairs is not currently supported"
    )
  if external_meshes:
    raise NotImplementedError(
        "External meshes are not currently supported in fallback lowering"
    )
  [jaxpr] = jaxprs
  [mesh] = meshes

  if compiler_params is not None:
    if hasattr(mesh, "dimension_semantics"):
      compiler_params = compiler_params.replace(
          dimension_semantics=mesh.dimension_semantics
      )

  num_scratch = len(jaxpr.invars) - len(in_nodes) - len(out_avals)
  scratch_avals = (
      [v.aval for v in jaxpr.invars[-num_scratch:]] if num_scratch > 0 else []
  )
  scratch_types = tuple(
      pallas_core.MemoryRef(v.inner_aval, v.memory_space) for v in scratch_avals
  )
  grid_spec = pallas_core.GridSpec(
      grid=tuple(mesh.shape.items()),
      in_specs=tuple(
          pallas_core.BlockSpec(
              memory_space=aval.memory_space
              if isinstance(aval, jax_core.ShapedArray)
              and not isinstance(aval.memory_space, jax_core.MemorySpace)
              else mesh.default_memory_space,
          )
          for aval in ctx.avals_in
      ),
      out_specs=tuple(
          pallas_core.BlockSpec(
              memory_space=aval.memory_space
              if isinstance(aval, jax_core.ShapedArray)
              and not isinstance(aval.memory_space, jax_core.MemorySpace)
              else mesh.default_memory_space,
          )
          for aval in out_avals
      ),
      scratch_shapes=scratch_types,
  )

  in_tree = tree_util.tree_structure(in_nodes)
  out_tree = tree_util.tree_structure(out_avals)

  in_origins = [f"arg{i}" for i in range(len(in_nodes))]
  out_origins = [f"out{i}" for i in range(len(out_avals))]

  _, grid_mapping = pallas_core.get_grid_mapping(
      grid_spec,
      [
          v.aval.inner_aval if isinstance(v.aval, state.AbstractRef) else v.aval
          for v in jaxpr.invars[: len(in_nodes)]
      ],
      in_tree,
      in_origins,
      [
          v.aval.inner_aval if isinstance(v.aval, state.AbstractRef) else v.aval
          for v in jaxpr.invars[len(in_nodes) : len(in_nodes) + len(out_avals)]
      ],
      out_tree,
      out_origins,
      debug=debug,
  )

  return pallas_call._pallas_call_lowering(
      ctx,
      *in_nodes,
      jaxpr=jaxpr,
      grid_mapping=grid_mapping,
      mesh=mesh,
      input_output_aliases=tuple(input_output_aliases.items()),
      debug=debug,
      interpret=interpret,
      compiler_params=compiler_params,
      cost_estimate=cost_estimate,
      out_avals=out_avals,
      metadata=metadata,
      name=name,
  )

