
def lower_jaxpr_into_pipelined_module(
    lowering_context: mlir.LoweringRuleContext,
    module: ir.Module,
    grid_mapping: pallas_core.GridMapping,
    jaxpr: jax_core.Jaxpr,
    *,
    name: str,
    dimension_semantics: Sequence[tpu_core.DimensionSemantics] | None,
    kernel_type: tpu_core.CoreType,
    mesh: mesh_lib.Mesh | None = None,
    dynamic_shape_replacement_enabled: bool = False,
    fuse_transposed_lhs_in_matmul: bool = False,
) -> None:
  backend = lowering_context.module_context.get_backend(optional=True)
  # NOTE: We should bump this periodically
  if backend is not None and is_cloud_tpu_older_than(2026, 4, 1, backend):
    platform_version = xla_bridge.get_backend().platform_version
    raise RuntimeError(
        "Pallas TPU requires a libtpu version that's at most a month old. Found"
        f" version string:\n{platform_version}"
    )
  debug_info = jaxpr.debug_info
  _mosaic_lowering_dynamic_shape_env = None
  if dynamic_shape_replacement_enabled:
    _mosaic_lowering_dynamic_shape_env = LoweringDynamicShapeEnv()

    def dynamic_shape_replacement_fn(
        shape: jax_core.Shape,
    ) -> tuple[Any, ...]:
      assert _mosaic_lowering_dynamic_shape_env is not None
      return tuple(
          _mosaic_lowering_dynamic_shape_env.to_placeholder(dim_expr)
          if jax_core.is_dim(dim_expr)
          else dim_expr
          for dim_expr in shape
      )

  else:
    dynamic_shape_replacement_fn = lambda x: x

  # Verify that we have legal block mappings to catch errors early.
  _check_block_mappings(
      grid_mapping.block_mappings, lowering_context, debug_info, kernel_type
  )

  mosaic_grid_mapping = MosaicGridMapping(
      jaxpr,
      grid_mapping,
      dimension_semantics,
      mesh,
      dynamic_shape_replacement_fn,
      kernel_type,
  )
  mosaic_grid_mapping.maybe_compress_grid()
  num_grid = len(mosaic_grid_mapping.grid_types)
  arg_types = [
      *mosaic_grid_mapping.grid_types,
      *mosaic_grid_mapping.scalar_prefetch_types,
      *mosaic_grid_mapping.operand_types,
      *mosaic_grid_mapping.scratch_types,
  ]

  def get_jaxpr_indices(grid_indices):
    return mosaic_grid_mapping.get_grid_indices(
        grid_indices, maybe_include_mapped_dims=False
    )

  cache = lowering_context.module_context.pallas_lowering_cache
  sym_tab = ir.SymbolTable(module.operation)

  def ctx_factory(jaxpr_indices):
    return PipelinedLoweringContext.from_mosaic_grid_mapping(
        mosaic_grid_mapping,
        jaxpr_indices,
        kernel_type=kernel_type,
        forward_compatible=lowering_context.is_forward_compat(),
        backend=backend,
        dynamic_shape_replacement_fn=dynamic_shape_replacement_fn,
        fuse_transposed_lhs_in_matmul=fuse_transposed_lhs_in_matmul,
        lowering_cache=cache,
        dynamic_shape_env=_mosaic_lowering_dynamic_shape_env,
    )

  with ir.InsertionPoint(module.body):
    func_op = _lower_jaxpr_to_func_common(
        jaxpr,
        name=name,
        arg_types=arg_types,
        num_grid=num_grid,
        get_jaxpr_indices=get_jaxpr_indices,
        ctx_factory=ctx_factory,
        dynamic_shape_replacement_enabled=dynamic_shape_replacement_enabled,
    )
  func_op.attributes["tpu.core_type"] = ir.Attribute.parse(
      f"#tpu.core_type<{kernel_type}>"
  )
  module.body.append(func_op)
  assert name not in sym_tab, f"Function name {name} already exists in symbol table."
  sym_tab.insert(func_op)
  window_params = []
  static_grid = None
  grid = mosaic_grid_mapping.grid
  if not grid and any(
      not bm.has_trivial_window() for bm in grid_mapping.block_mappings
  ):
    raise NotImplementedError(
        "Non-trivial windowing is not supported for grid-free pallas_call."
    )
  if grid:
    for i, bm in enumerate(grid_mapping.block_mappings):
      func_name = f"transform_{i}"
      # ANY and SEMAPHORE operands don't support windowing and require empty window_params.
      block_memory_space = bm.block_aval.memory_space
      if block_memory_space is None:
        block_memory_space = pallas_core.MemorySpace.DEFAULT
      tpu_memory_space = tpu_core.memory_space_to_tpu_memory_space(
          block_memory_space, kernel_type
      )
      if (
          tpu_memory_space is ANY
          or tpu_memory_space == tpu_core.MemorySpace.HBM
          or tpu_memory_space == tpu_core.MemorySpace.SEMAPHORE
      ):
        # We checked above that the block does not require windowing.
        window_params.append(ir.DictAttr.get())
        continue

      with ir.InsertionPoint(module.body):
        mlir_func = lower_jaxpr_to_transform_func(
            bm.index_map_jaxpr.jaxpr,
            bm.block_aval,
            name=func_name,
            mosaic_grid_mapping=mosaic_grid_mapping,
            kernel_type=kernel_type,
            forward_compatible=lowering_context.is_forward_compat(),
            dynamic_shape_replacement_fn=dynamic_shape_replacement_fn,
            backend=backend,
            lowering_cache=cache,
            dynamic_shape_env=_mosaic_lowering_dynamic_shape_env,
        )
      assert mlir_func.verify(), mlir_func
      block_shape = list(pallas_core._get_block_shape(bm.block_shape))

      # Force single-buffering pipelining for trivial windowing in VMEM.
      pipeline_mode = bm.pipeline_mode
      if (
          tpu_memory_space == tpu_core.MemorySpace.VMEM
          and bm.has_trivial_window()
      ):
        pipeline_mode = pallas_core.Buffered(1)

      # If we have an extended dtype, we need to add the block shape for the
      # remaining physical dtype.
      block_shape += list(_get_aval_physical_dtype_shape(bm.block_aval.inner_aval))
      block_shape = dynamic_shape_replacement_fn(block_shape)
      window_shape = ir.DenseI64ArrayAttr.get(block_shape)
      block_params: dict[str, ir.Attribute] = dict(
          window_bounds=window_shape,
          transform_indices=ir.FlatSymbolRefAttr.get(func_name),
      )
      for bd in bm.block_shape:
        if not isinstance(
            bd, (pallas_core.Element, pallas_core.Squeezed, pallas_core.Blocked)
        ):
          raise NotImplementedError(
              "Unsupported block dimension type: "
              f"{type(bd)} for block shape: {bm.block_shape}"
          )
      is_element_block = [isinstance(bd, pallas_core.Element)
                          for bd in bm.block_shape]
      if any(is_element_block):
        is_element_or_squeezed_block = [
            isinstance(bd, (pallas_core.Element, pallas_core.Squeezed))
            for bd in bm.block_shape
        ]
        if not all(is_element_or_squeezed_block):
          raise NotImplementedError(
              "All block dimensions must be Elements or none of them can be"
              " Elements."
          )
        padding = [
            bd.padding if isinstance(bd, pallas_core.Element) else (0, 0)
            for bd in bm.block_shape
        ]
        pad_low, pad_high = map(list, zip(*padding))
        block_params["window_kind"] = ir.Attribute.parse(
            f"#tpu.element_window<{pad_low},{pad_high}>"
        )
      if pipeline_mode is not None:
        if not isinstance(pipeline_mode, pallas_core.Buffered):
          raise LoweringException(
              f"Unsupported pipeline mode: {pipeline_mode}."
          )
        if pipeline_mode.use_lookahead:
          raise NotImplementedError(
              "Lookahead is not supported for XLA pipeline emitter lowering."
          )
        buffer_count = pipeline_mode.buffer_count
        if buffer_count < 1 or buffer_count > 2:
          raise LoweringException(
              "Only single (1) and double (2) buffering are supported. Got"
              f" {buffer_count}."
          )
        pipeline_mode_str = "synchronous" if buffer_count == 1 else "double_buffered"
        block_params["pipeline_mode"] = ir.Attribute.parse(
            f"#tpu.pipeline_mode<{pipeline_mode_str}>"
        )
        if pipeline_mode.revisit is not None:
          if (
              pipeline_mode.revisit == pallas_core.RevisitMode.ANY
              and buffer_count > 1
          ):
            raise LoweringException(
                "RevisitMode.ANY is not supported with double buffering."
            )
          block_params["revisit_mode"] = ir.Attribute.parse(
              f"#tpu.revisit_mode<{pipeline_mode.revisit.value}>"
          )
      window_params.append(ir.DictAttr.get(block_params))
      module.body.append(mlir_func)
      sym_tab.insert(mlir_func)
    func_op.attributes["window_params"] = ir.ArrayAttr.get(window_params)

    static_grid = [
        MLIR_DYNAMIC if b is pallas_core.dynamic_grid_dim else b for b in grid
    ]
    static_grid = dynamic_shape_replacement_fn(static_grid)
    func_op.attributes["iteration_bounds"] = ir.DenseI64ArrayAttr.get(static_grid)
  func_op.attributes["scalar_prefetch"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), len(mosaic_grid_mapping.scalar_prefetch_types))
  func_op.attributes["scratch_operands"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), len(mosaic_grid_mapping.scratch_types))
  func_op.attributes["dimension_semantics"] = (
      mosaic_grid_mapping.get_dimension_semantics()
  )
  if dynamic_shape_replacement_enabled:
    if _mosaic_lowering_dynamic_shape_env is None:
      raise ValueError(
          "Dynamic shape env is None, invariant violated. Unreachable?"
      )

    # Now we can use jax to compute the dynamic shape graph

    if static_grid is not None:
      grid_vars = [
          _mosaic_lowering_dynamic_shape_env.placeholder_to_dim_expr.get(g, g)
          for g in static_grid
      ]
    else:
      grid_vars = []

    invars = cast(
        list[jax_core.ShapedArray], [invar.aval for invar in jaxpr.invars]
    )
    # Faux shape for grid, just to get the avals
    invars.append(jax_core.ShapedArray(grid_vars, jnp.int32))
    args_dimvars = shape_poly.all_dim_vars(invars)

    # This is dimexpr var -> placeholder value for when we jit the dim expr
    env: dict[str, Any] = {}
    for aval in args_dimvars:
      env[aval] = _mosaic_lowering_dynamic_shape_env.to_placeholder(aval)

    # We store the location of each dimvar, so we can map it back
    # to the argument and dimension index. During specialization phase of Mosaic
    # use this information to grab the concrete value from specialized TPU
    # custom call and replace the placeholder.
    # TODO(slebedev): Use a TypedDict here.
    location_of_dimvar: dict[str, dict[str, int]] = {}

    # Populate location_of_dimvar from input shapes.
    for operand_idx, aval in enumerate(lowering_context.avals_in):
      for dimension_idx, dim in enumerate(getattr(aval, "shape", [])):
        location_of_dimvar.setdefault(
            str(dim),
            {"operand_index": operand_idx, "dimension_index": dimension_idx},
        )

    # Dynamic grid bounds have to go at the front.
    if mosaic_grid_mapping.grid:
      dynamic_dims = (
          d for d in mosaic_grid_mapping.grid if pallas_core.is_dynamic_dim(d)
      )
      for operand_idx, dim in enumerate(dynamic_dims):
        location_of_dimvar.setdefault(
            str(dim), {"operand_index": operand_idx, "dimension_index": -1}
        )

    for (
        placeholder,
        dim_expr,
    ) in _mosaic_lowering_dynamic_shape_env.placeholder_to_dim_expr.items():
      top_level_names = list(env.keys())
      if dim_expr not in top_level_names:
        jitted_eval = jax.jit(
            jax_core.evaluate_shape,
            static_argnames=(
                "shape",
                "dim_vars",
            ),
            keep_unused=True,
        )
        stablehlo = export(
            jitted_eval, platforms=[str(jax.devices()[0].platform)]
        )(
            (dim_expr,), tuple(args_dimvars), *(env[v] for v in args_dimvars)
        ).mlir_module()
        arg_names = args_dimvars
        # See Note - On Export Placeholders for more details.
        module.operation.attributes[
            "tpu.dynamic_dimension_mapping_module_" + str(placeholder)
        ] = ir.StringAttr.get(stablehlo)
        arg_locs_attr = []
        for arg_name in arg_names:
          if arg_name not in location_of_dimvar:
            raise ValueError(
                f"Unable to find location of dimvar {arg_name} in dim_map"
                f" {location_of_dimvar}"
            )
          loc = location_of_dimvar[arg_name]
          op_idx = ir.IntegerAttr.get(
              ir.IntegerType.get_signless(64), loc["operand_index"]
          )
          dim_idx = ir.IntegerAttr.get(
              ir.IntegerType.get_signless(64), loc["dimension_index"]
          )
          loc_attr = ir.DictAttr.get({
              "operand_index": op_idx,
              "dimension_index": dim_idx,
          })
          arg_locs_attr.append(loc_attr)
        module.operation.attributes[
            "tpu.dynamic_dimension_mapping_indices_" + str(placeholder)
        ] = ir.ArrayAttr.get(arg_locs_attr)

