
def _cached_lowering_to_hlo(
    closed_jaxpr: core.ClosedJaxpr, module_name, backend, num_const_args: int,
    in_avals, semantic_in_shardings, semantic_out_shardings,
    in_layouts, out_layouts, num_devices, device_assignment, donated_invars,
    all_default_mem_kind, inout_aliases: None | tuple[None | int, ...],
    propagated_out_mem_kinds: tuple[None | str, ...], platforms: tuple[str, ...],
    lowering_parameters: mlir.LoweringParameters,
    abstract_mesh: AbstractMesh | None):
  # in_avals, in_shardings, in_layouts include the jaxpr_const_args(jaxpr)
  out_avals = closed_jaxpr.out_avals
  jaxpr = closed_jaxpr.jaxpr
  in_shardings = semantic_in_shardings.shardings
  out_shardings = semantic_out_shardings.shardings

  log_priority = logging.WARNING if config.log_compiles.value else logging.DEBUG
  if logger.isEnabledFor(log_priority):
    logger.log(log_priority,
               "Compiling %s with global shapes and types %s. "
               "Argument mapping: %s.",
               module_name, in_avals, in_shardings)

  in_mlir_shardings = map(_to_logical_sharding, in_avals, in_shardings)
  out_mlir_shardings = map(_to_logical_sharding, out_avals, out_shardings)
  replicated_args = [False] * len(in_avals)
  axis_ctx = sharding_impls.ShardingContext(num_devices, device_assignment,
                                            abstract_mesh)

  if num_devices > 1:
    unsupported_effects = effects.ordered_effects.filter_in(closed_jaxpr.effects)
    unsupported_effects = effects.shardable_ordered_effects.filter_not_in(
        unsupported_effects)
    if len(unsupported_effects) > 0:
      raise ValueError(
        "The following ordered effects are not supported for "
        f"more than 1 device: {unsupported_effects}")
  ordered_effects = list(effects.ordered_effects.filter_in(closed_jaxpr.effects))
  arg_names = ("",) * num_const_args + jaxpr._debug_info.safe_arg_names(len(in_avals) - num_const_args)
  with dispatch.log_elapsed_time(
        "Finished jaxpr to MLIR module conversion {fun_name} in {elapsed_time:.9f} sec",
        fun_name=module_name, event=dispatch.JAXPR_TO_MLIR_MODULE_EVENT):
    lowering_result = mlir.lower_jaxpr_to_module(
        module_name,
        closed_jaxpr,
        num_const_args=num_const_args,
        ordered_effects=ordered_effects,
        backend=backend,
        platforms=platforms,
        axis_context=axis_ctx,
        in_avals=in_avals,
        donated_args=donated_invars,
        replicated_args=replicated_args,
        arg_shardings=in_mlir_shardings,
        result_shardings=out_mlir_shardings,
        in_layouts=in_layouts,
        out_layouts=out_layouts,
        arg_names=arg_names,
        result_names=jaxpr._debug_info.safe_result_paths(len(out_avals)),
        num_partitions=num_devices,
        all_default_mem_kind=all_default_mem_kind,
        input_output_aliases=inout_aliases,
        propagated_out_mem_kinds=propagated_out_mem_kinds,
        lowering_parameters=lowering_parameters)
  tuple_args = dispatch.should_tuple_args(len(in_avals), backend.platform)
  unordered_effects = list(
      effects.ordered_effects.filter_not_in(closed_jaxpr.effects))
  return (lowering_result.module, lowering_result.keepalive,
          lowering_result.host_callbacks, unordered_effects, ordered_effects,
          tuple_args, lowering_result.shape_poly_state)

