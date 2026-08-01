
def _call_exported_lowering(ctx: mlir.LoweringRuleContext, *args,
                            exported: Exported):
  _ensure_backends_initialized(exported.platforms)
  if exported.uses_global_constants:
    ctx.module_context.shape_poly_state.uses_dim_vars = True
  with ctx.module_context.module.context:
    submodule = exported.mlir_module(serialized=False)

  symtab = ir.SymbolTable(submodule.operation)
  shardy_enabled = has_sdy_mesh(symtab, submodule)
  if shardy_enabled:
    if not config.use_shardy_partitioner.value:
      raise ValueError(
          "The function was exported with shardy enabled but you are calling "
          "it with Shardy disabled. Please enable Shardy using "
          "`--jax_use_shardy_partitioner=True`.")
    # TODO(b/422690222): remove this pass once we don't need to support 6m
    # old exported modules.
    if has_sdy_meshes_in_frontend_attributes(submodule):
      with submodule.context:
        pipeline = passmanager.PassManager.parse(
            'builtin.module(xla-sdy-round-trip-import-shardy-attrs)')
        pipeline.run(submodule.operation)

  with submodule.context:
    pipeline = passmanager.PassManager.parse(
        'builtin.module(sdy-lift-inlined-meshes)')
    pipeline.run(submodule.operation)
  mesh = None
  if shardy_enabled:
    mesh = get_mesh_from_symbol(symtab)

  axis_context = ctx.module_context.axis_context
  if isinstance(axis_context, sharding_impls.ShardingContext):
    num_devices = axis_context.num_devices
  elif isinstance(axis_context, sharding_impls.SPMDAxisContext):
    num_devices = axis_context.mesh.size
  else:
    raise NotImplementedError(type(axis_context))
  if num_devices != exported.nr_devices and exported.nr_devices != 1:
    raise ValueError(
        f"Function {exported.fun_name} was exported for "
        f"{exported.nr_devices} devices and is called in a context with "
        f"{num_devices} devices, which is not allowed."
    )

  # Apply in_shardings
  in_avals = [core.physical_aval(a)
              if dtypes.issubdtype(a.dtype, dtypes.extended) else a  # type: ignore
              for a in ctx.avals_in]
  exported_in_avals = [core.physical_aval(a)
                       if dtypes.issubdtype(a.dtype, dtypes.extended) else a
                       for a in exported.in_avals]
  if exported._has_named_shardings:
    args = tuple(
        wrap_with_sharding(
            ctx, x, x_aval,
            _get_named_sharding(exported._has_named_shardings,
                                named_sharding, None, x_aval, None),  # type: ignore
            use_shardy=True)
        for x, named_sharding, x_aval in zip(
          args, exported._in_named_shardings, exported_in_avals))
  elif mesh:
    # A mesh only exists if Shardy is enabled, or we saved named shardings.
    args = tuple(
        wrap_with_sharding(
            ctx, x, x_aval,
            _get_named_sharding(False, None, hlo_sharding, x_aval, mesh),  # type: ignore
            use_shardy=True)
        for x, hlo_sharding, x_aval in zip(
          args, exported.in_shardings_hlo, exported_in_avals))
  else:
    # Since there is no mesh - either due to shardy being disabled or the loaded
    # function being lowered for GSPMD (so no shardy mesh) - need to create a
    # GSPMD sharding from the HLO sharding (can't use shardy lowering).
    args = tuple(
        wrap_with_sharding(ctx, x, x_aval, x_sharding, use_shardy=False)
        for x, x_aval, x_sharding in zip(
          args, in_avals, exported.in_shardings_hlo))

  # The called function may have been exported with polymorphic shapes and called
  # now with more refined shapes. We insert hlo.ConvertOp to ensure the module
  # is valid.
  def convert_shape(x: ir.Value, x_aval: core.AbstractValue,
                    new_aval: core.AbstractValue) -> ir.Value:
    new_ir_type = mlir.aval_to_ir_type(ctx.module_context, new_aval)
    if x.type != new_ir_type:
      return hlo.convert(new_ir_type, x)
    else:
      return x

  main = cast(func_dialect.FuncOp, symtab["main"])
  callee_type = main.type
  # TODO: maybe cache multiple calls
  fn = mlir.merge_mlir_modules(ctx.module_context.module,
                               f"call_exported_{exported.fun_name}",
                               submodule,
                               dst_symtab=ctx.module_context.symbol_table)

  submodule_args: list[ir.Value] = []
  # All the platforms for the current lowering must be among the platforms
  # for which the callee was lowered.
  lowering_platforms = ctx.module_context.platforms

  callee_lowering_platform_index: list[int] = []
  for platform in lowering_platforms:
    if platform in exported.platforms:
      callee_lowering_platform_index.append(
        exported.platforms.index(platform))
    elif DisabledSafetyCheck.platform() in exported.disabled_safety_checks:
      callee_lowering_platform_index.append(0)
    else:
      raise ValueError(
          f"Function '{exported.fun_name}' was exported for "
          f"platforms '{exported.platforms}' but it is used "
          f"on '{lowering_platforms}'.")

  if len(exported.platforms) > 1:
    # The exported module takes a platform index argument
    if len(lowering_platforms) > 1:
      current_platform_idx = ctx.dim_var_values[0]
    else:
      current_platform_idx = cast(ir.Value, mlir.ir_constant(np.int32(0)))
    # Compute the rule index based on the current platform
    i32_type = mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray((), dtype=np.int32))
    if current_platform_idx.type != i32_type:
      current_platform_idx = hlo.convert(i32_type, current_platform_idx)
    callee_platform_idx = hlo.CaseOp([i32_type],
                                     index=current_platform_idx,
                                     num_branches=len(lowering_platforms))
    for i in range(len(lowering_platforms)):
      branch = callee_platform_idx.regions[i].blocks.append()
      with ir.InsertionPoint(branch):
        hlo.return_([mlir.ir_constant(
          np.int32(callee_lowering_platform_index[i]))])
    if callee_platform_idx.result.type != callee_type.inputs[0]:
      callee_platform_idx = hlo.ConvertOp(callee_type.inputs[0],
                                          callee_platform_idx.result)

    submodule_args.append(callee_platform_idx.result)
  else:
    assert len(lowering_platforms) == 1

  ordered_effects = exported.ordered_effects
  for eff in ordered_effects:
    token_in = ctx.tokens_in.get(eff)
    submodule_args.append(token_in)
  kept_args = [
      convert_shape(a, a_aval, exported_in_aval)
      for i, (a, a_aval, exported_in_aval) in enumerate(zip(args, in_avals, exported_in_avals))
      if i in exported.module_kept_var_idx]
  submodule_args = submodule_args + kept_args

  call = func_dialect.CallOp(callee_type.results,
                             ir.FlatSymbolRefAttr.get(fn),
                             submodule_args)
  if ordered_effects:
    tokens_out = {eff: (call.results[effect_idx],)
                  for effect_idx, eff in enumerate(ordered_effects)}
    ctx.set_tokens_out(mlir.TokenSet(tokens_out))

  out_avals = [core.physical_aval(a)
               if dtypes.issubdtype(a.dtype, dtypes.extended) else a
               for a in ctx.avals_out]
  # The ctx.avals_out already contain the abstract values refined by
  # _call_exported_abstract_eval.
  results = tuple(
      convert_shape(out, out_aval, refined_out_aval)
      for out, out_aval, refined_out_aval in zip(
          call.results[len(ordered_effects):], exported.out_avals, out_avals))
  # Apply out_shardings
  if exported._has_named_shardings:
    results = tuple(
        wrap_with_sharding(
            ctx, x, x_aval,
            _get_named_sharding(True, x_sharding, None, x_aval, None),  # type: ignore
            use_shardy=True)
        for x, x_aval, x_sharding in zip(
            results, out_avals, exported._out_named_shardings))
  elif mesh:
    results = tuple(
        wrap_with_sharding(
            ctx, x, x_aval,
            _get_named_sharding(False, None, x_sharding, x_aval, mesh),  # type: ignore
            use_shardy=True)
        for x, x_aval, x_sharding in zip(
            results, out_avals, exported.out_shardings_hlo))
  else:
    # Since there is no mesh - either due to shardy being disabled or the loaded
    # function being lowered for GSPMD (so no shardy mesh) - need to create a
    # GSPMD sharding from the HLO sharding (can't use shardy lowering).
    results = tuple(
        wrap_with_sharding(ctx, x, x_aval, x_sharding, use_shardy=False)
        for x, x_aval, x_sharding in zip(
            results, out_avals, exported.out_shardings_hlo))
  return results

