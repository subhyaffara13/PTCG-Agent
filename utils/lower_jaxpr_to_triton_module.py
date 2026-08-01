
def lower_jaxpr_to_triton_module(
    jaxpr: jax_core.Jaxpr,
    grid_mapping: GridMapping,
    platform: str,
    compute_capability: int | None,
    mlir_ctx: mlir.ModuleContext,
) -> LoweringResult:
  debug_info = jaxpr.debug_info
  if grid_mapping.num_dynamic_grid_bounds:
    raise NotImplementedError(
        "dynamic grid bounds not supported in the Triton backend"
    )
  if grid_mapping.num_index_operands:
    raise NotImplementedError(
        "scalar prefetch not implemented in the Triton backend"
    )
  if jaxpr.invars[grid_mapping.slice_scratch_ops]:
    raise NotImplementedError(
        "scratch memory not implemented in the Triton backend"
    )
  with _new_ir_context(), ir.Location.unknown():
    module = ir.Module.create()
    attrs = module.operation.attributes
    module_name = mlir.sanitize_name(debug_info.func_name)
    attrs["sym_name"] = ir.StringAttr.get(module_name)
    new_mlir_ctx = mlir.ModuleContext(
        platforms=mlir_ctx.platforms,
        backend=mlir_ctx.backend,
        axis_context=mlir_ctx.axis_context,
        keepalives=mlir_ctx.keepalives,
        channel_iterator=mlir_ctx.channel_iterator,
        host_callbacks=mlir_ctx.host_callbacks,
        lowering_parameters=mlir_ctx.lowering_parameters,
        context=ir.Context.current,
        module=module,
        ip=ir.InsertionPoint(module.body),
    )
    param_types = [
        # pyrefly: ignore[missing-attribute]
        tt_dialect.PointerType.get(_dtype_to_ir_type(var.aval.dtype), 1)
        for var in jaxpr.invars
    ]
    assert len(jaxpr.outvars) == 0
    fn_type = ir.FunctionType.get(param_types, [])
    fn = tt_dialect.FuncOp(
        module_name,
        ir.TypeAttr.get(fn_type),
        sym_visibility="public",
        res_attrs=ir.DictAttr.get(dict(noinline=ir.BoolAttr.get(False))),
        ip=ir.InsertionPoint.at_block_begin(module.body),
    )
    fn.arg_attrs = ir.ArrayAttr.get(
        [ir.DictAttr.get({"tt.divisibility": mlir.i32_attr(32)})]
        * len(param_types)
    )
    fn.body.blocks.append(*fn_type.inputs)
    [entry] = fn.body.blocks
    with ir.InsertionPoint(entry):
      new_grid, program_ids = _process_grid_to_3d_grid(grid_mapping)
      local_program_ids = [
          pid
          for i, pid in enumerate(program_ids)
          if i not in grid_mapping.vmapped_dims
      ]
      ctx = ModuleContext(
          mlir.sanitize_name(debug_info.func_name),
          grid_mapping,
          local_program_ids,
          mlir.TracebackCaches(),
          platform,
          compute_capability,
          mlir_ctx=new_mlir_ctx,
      )
      block_infos = [
          BlockInfo(
              block_mapping.array_aval,
              _eval_index_map(ctx, program_ids, block_mapping),
              _get_index_alignment(block_mapping),
              tuple(pallas_core.squeezed if isinstance(b, pallas_core.Squeezed)
                    else pallas_core._get_block_dim_size(b)
                    for b in block_mapping.block_shape),
          )
          for block_mapping in grid_mapping.block_mappings
      ]
      () = lower_jaxpr_to_triton_ir(ctx, jaxpr, block_infos, *entry.arguments)
      tt_dialect.return_([])
    return LoweringResult(module, new_grid)

