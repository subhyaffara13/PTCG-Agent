import json

def _lower_to_custom_call(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    mosaic_module: ir.Module,
    mosaic_params: tpu_core.CompilerParams,
    kernel_type: tpu_core.CoreType | None,
    num_dynamic_grid_bounds: int,
    input_output_aliases: tuple[tuple[int, int], ...],
    cost_estimate: pallas_core.CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    effects: jax_core.Effects,
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str,
    jax_mesh,
):
  input_output_aliases = tuple(
      (a[0] + num_dynamic_grid_bounds, a[1]) for a in input_output_aliases
  )

  # Replace in_avals to physical avals.
  # This step is required for mapping logical types to physical types.
  # (e.g. PRNG key -> uint32[2])
  physical_avals = [jax_core.physical_aval(aval) for aval in ctx.avals_in]
  physical_out_avals = [jax_core.physical_aval(aval) for aval in ctx.avals_out]
  ctx = ctx.replace(avals_in=physical_avals, avals_out=physical_out_avals)

  # Booleans are loaded into the kernel as integers.
  def _maybe_cast_inputs(*args):
    args = [_jax_value_to_mosaic_value(x) for x in args]
    return args

  kernel_in_avals = [_jaxpr_kernel_aval_to_mosaic(x) for x in physical_avals]
  kernel_out_avals = [
      _jaxpr_kernel_aval_to_mosaic(x) for x in physical_out_avals
  ]
  cast_ctx = ctx.replace(avals_out=kernel_in_avals)
  in_nodes = mlir.lower_fun(_maybe_cast_inputs)(cast_ctx, *in_nodes)

  # Dynamic grid bounds have to go at the front.
  dynamic_grid_args, args = (
      in_nodes[:num_dynamic_grid_bounds],
      in_nodes[num_dynamic_grid_bounds:],
  )
  kernel_ctx = ctx.replace(avals_in=kernel_in_avals, avals_out=kernel_out_avals)
  input_memory_spaces, output_memory_spaces = _resolve_memory_spaces(
      ctx.avals_in,
      out_avals,
      input_output_aliases=input_output_aliases,
      kernel_type=kernel_type,
  )

  if cost_estimate is not None:
    mosaic_cost_estimate = cast(
        tpu_custom_call.CostEstimate, dataclasses.asdict(cost_estimate)
    )
  else:
    mosaic_cost_estimate = None

  dict_metadata = dict(metadata) if metadata is not None else {}
  del metadata
  if jax_mesh is not None:
    mesh_axes = {
        e.name
        for e in effects
        if isinstance(e, jax_core.NamedAxisEffect)
        # Filter for only device mesh axis name effects
        and e.name in jax_mesh.axis_names
    }
    # Only put mesh axes in metadata if there are any.
    if mesh_axes:
      if "mesh_axes" in dict_metadata:
        raise ValueError("Metadata already contains mesh axes.")
      mesh_axes_list = list(mesh_axes)
      if all(isinstance(a, str) for a in mesh_axes):
        mesh_axes_list = sorted(mesh_axes)  # pyrefly: ignore[bad-specialization]
      dict_metadata["mesh_axes"] = json.dumps(mesh_axes_list)
  out_nodes = mosaic.lower_module_to_custom_call(
      kernel_ctx,
      *dynamic_grid_args,
      *args,
      module=mosaic_module,
      out_type=kernel_out_avals,
      kernel_name=mlir.sanitize_name(name),
      cost_estimate=mosaic_cost_estimate,
      vmem_limit_bytes=mosaic_params.vmem_limit_bytes,
      flags=mosaic_params.flags,
      allow_input_fusion=mosaic_params.allow_input_fusion,
      input_output_aliases=input_output_aliases,
      serialization_format=mosaic_params.serialization_format,
      internal_scratch_in_bytes=mosaic_params.internal_scratch_in_bytes,
      collective_id=mosaic_params.collective_id,
      has_side_effects=_resolve_side_effect_type(
          mosaic_params.has_side_effects
      ),
      output_memory_spaces=output_memory_spaces,
      disable_bounds_checks=mosaic_params.disable_bounds_checks,
      disable_semaphore_checks=mosaic_params.disable_semaphore_checks,
      input_memory_spaces=input_memory_spaces,
      metadata=dict_metadata,
      skip_device_barrier=mosaic_params.skip_device_barrier,
      allow_collective_id_without_custom_barrier=mosaic_params.allow_collective_id_without_custom_barrier,
      shape_invariant_numerics=mosaic_params.shape_invariant_numerics,
      needs_layout_passes=mosaic_params.needs_layout_passes,
      tiling=_resolve_tiling(mosaic_params, kernel_type),
  )
  _maybe_cast_to_bool = (
      lambda x, aval: x.astype(jax.numpy.bool_)
      if aval.dtype == jax.numpy.bool_
      else x
  )

  def _maybe_cast_outputs(*args):
    args = [_maybe_cast_to_bool(x, aval) for x, aval in zip(args, out_avals)]
    return args

  cast_ctx = ctx.replace(avals_in=kernel_out_avals)
  return mlir.lower_fun(_maybe_cast_outputs)(cast_ctx, *out_nodes)

