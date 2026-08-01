
def pallas_call_tpu_lowering_rule(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    jaxpr: jax_core.Jaxpr,
    grid_mapping: pallas_core.GridMapping,
    mesh: pallas_core.Mesh | None,
    input_output_aliases: tuple[tuple[int, int], ...],
    debug: bool,
    interpret: bool,
    compiler_params: pallas_core.CompilerParams | None,
    cost_estimate: pallas_core.CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str | None,
):
  """Lowers a pallas_call to a Mosaic TPU custom call."""
  del interpret  # Unused.

  debug_info = jaxpr.debug_info
  if debug:
    print(f"\nThe kernel jaxpr for pallas_call {debug_info.func_src_info}:")
    print(jaxpr)

  if compiler_params is None:
    mosaic_params = tpu_core.CompilerParams()
  else:
    assert isinstance(compiler_params, tpu_core.CompilerParams)
    mosaic_params = compiler_params

  jax_mesh = None
  axis_context = ctx.module_context.axis_context
  if axis_context is not None:
    if isinstance(axis_context, sharding_impls.SPMDAxisContext):
      jax_mesh = axis_context.mesh
  mlir_ctx = ctx.module_context.context
  tpu.register_dialect(mlir_ctx)

  with mlir_ctx, ir.Location.unknown(mlir_ctx):
    mosaic_module = lowering.lower_jaxpr_to_pipelined_module(
        ctx,
        grid_mapping,
        jaxpr,
        dimension_semantics=mosaic_params.dimension_semantics,
        kernel_type=tpu_core.CoreType.TC,
        mesh=jax_mesh,
        dynamic_shape_replacement_enabled=pallas_core.dynamic_shapes_export_enabled(),
        fuse_transposed_lhs_in_matmul=mosaic_params.fuse_transposed_lhs_in_matmul,
    )

  if debug:
    pm = passmanager.PassManager.parse("builtin.module(canonicalize)", mlir_ctx)
    pm.run(mosaic_module.operation)
    print(f"\nThe Mosaic module for pallas_call {debug_info.func_src_info}:")
    print(mosaic_module)

  return _lower_to_custom_call(
      ctx,
      *in_nodes,
      mosaic_module=mosaic_module,
      mosaic_params=mosaic_params,
      kernel_type=tpu_core.CoreType.TC,
      num_dynamic_grid_bounds=grid_mapping.num_dynamic_grid_bounds,
      input_output_aliases=input_output_aliases,
      cost_estimate=cost_estimate,
      out_avals=out_avals,
      effects=jaxpr.effects,
      metadata=metadata,
      name=name or debug_info.func_name,
      jax_mesh=jax_mesh,
  )

