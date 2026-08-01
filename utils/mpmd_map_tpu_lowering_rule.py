
def mpmd_map_tpu_lowering_rule(
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
    num_scratch,
):
  del interpret  # Unused.

  if debug:
    for idx, jaxpr in enumerate(jaxprs):
      print(
          f"\nThe kernel jaxpr {idx=} for mpmd_map"
          f" {jaxpr.debug_info.func_src_info}:"
      )
      print(jaxpr)

  if compiler_params is None:
    mosaic_params = tpu_core.CompilerParams()
  else:
    assert isinstance(compiler_params, tpu_core.CompilerParams)
    mosaic_params = compiler_params

  # TODO(slebedev): Check kernel type and raise if it is set.
  if mosaic_params.dimension_semantics is not None:
    raise ValueError(
        "mpmd_map does not support dimension_semantics= in compiler_params="
    )

  mpmd_meshes_map = {
      mesh.core_type: mesh for mesh in [*meshes, *external_meshes]
  }
  jax_mesh = None
  axis_context = ctx.module_context.axis_context
  if axis_context is not None:
    if isinstance(axis_context, sharding_impls.SPMDAxisContext):
      jax_mesh = axis_context.mesh
  mlir_ctx = ctx.module_context.context
  tpu.register_dialect(mlir_ctx)

  some_jaxpr = jaxprs[0]
  is_scalar_input = [
      isinstance(v.aval, jax_core.ShapedArray) and not v.aval.shape
      for v in some_jaxpr.invars
  ]

  with mlir_ctx, ir.Location.unknown(mlir_ctx):
    mosaic_module = ir.Module.create()
    for mesh, jaxpr in zip(meshes, jaxprs, strict=True):
      if not hasattr(mesh, "core_type") or not hasattr(
          mesh, "dimension_semantics"
      ):
        raise ValueError(
            "mpmd_map requires the mesh to define its ``core_type`` and"
            " ``dimension_semantics``"
        )

      match kernel_type := mesh.core_type:
        case tpu_core.CoreType.TC:
          if mpmd_meshes_map is not None and mpmd_meshes_map.keys() != {
              tpu_core.CoreType.TC
          }:
            raise NotImplementedError(
                "mpmd_map does not support TC kernels yet."
            )
        case (
            tpu_core.CoreType.SC_SCALAR_SUBCORE
            | tpu_core.CoreType.SC_VECTOR_SUBCORE
        ):
          if not tpu_info.is_tpu_device():
            raise ValueError(
                "SparseCore kernels are only supported on TPU, but the current"
                f" device is {tpu_info.get_device_kind()}."
            )
          info = tpu_info.get_tpu_info()
          if not info.sparse_core:
            raise ValueError(
                "SparseCore is not available on the current device"
                f" ({info.chip_version}), but the kernel type is set to"
                " SparseCore."
            )
        case _:
          raise ValueError(f"Unsupported kernel type: {kernel_type}")

      if any(is_scalar_input):
        jaxpr = _rewrite_jaxpr_for_lowering(
            jaxpr, mesh, (*meshes, *external_meshes)
        )

      lowering.lower_jaxpr_into_unpipelined_module(
          ctx,
          mosaic_module,
          jaxpr,
          jax_mesh=jax_mesh,
          pallas_mesh=mesh,
          name=mlir.sanitize_name(jaxpr.debug_info.func_name),
          dynamic_shape_replacement_enabled=pallas_core.dynamic_shapes_export_enabled(),
          num_scratch=num_scratch,
          needs_layout_passes=mosaic_params.needs_layout_passes,
      )

  if debug:
    pm = passmanager.PassManager.parse("builtin.module(canonicalize)", mlir_ctx)
    pm.run(mosaic_module.operation)
    print("\nThe Mosaic module for mpmd_map:")
    print(mosaic_module)

  if name is None:
    name = "_".join(jaxpr.debug_info.func_name for jaxpr in jaxprs)

  match [*{mesh.core_type for mesh in meshes}]:
    case [kernel_type]:
      pass
    case _:
      # Use a stub ``kernel_type`` if we are lowering multiple kernels.
      # This will hopefully cause a runtime error if ``kernel_type`` is ever
      # accessed.
      kernel_type = None

  def _maybe_expand_scalar_input(is_scalar, in_node, aval):
    expand_ctx = ctx.replace(
        avals_in=[aval],
        avals_out=[aval.update(shape=(1,))]
    )
    if is_scalar:
      return mlir.lower_fun(lambda x: x[None], multiple_results=False)(
          expand_ctx, in_node
      )[0]
    return in_node
  in_nodes = [
      _maybe_expand_scalar_input(is_scalar, in_node, aval)
      for is_scalar, in_node, aval in zip(is_scalar_input, in_nodes, ctx.avals_in)
  ]
  ctx = ctx.replace(
      avals_in=[
          aval.update(shape=(1,))
          if is_scalar
          else aval
          for is_scalar, aval in zip(is_scalar_input, ctx.avals_in)
      ]
  )

  return _lower_to_custom_call(
      ctx,
      *in_nodes,
      mosaic_module=mosaic_module,
      mosaic_params=mosaic_params,
      kernel_type=kernel_type,
      num_dynamic_grid_bounds=0,
      input_output_aliases=tuple(input_output_aliases.items()),
      cost_estimate=cost_estimate,
      out_avals=out_avals,
      effects=set().union(*(jaxpr.effects for jaxpr in jaxprs)),
      metadata=metadata,
      name=name,
      jax_mesh=jax_mesh,
  )

