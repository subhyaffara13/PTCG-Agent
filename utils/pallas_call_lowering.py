
def pallas_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *args,
    jaxpr: jax_core.Jaxpr,
    interpret: bool,
    debug: bool,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: pallas_core.GridMapping,
    mesh: pallas_core.Mesh | None,
    compiler_params: pallas_core.CompilerParams | None,
    cost_estimate: pallas_core.CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str | None,
):
  del metadata, name  # TODO(sharadmv): Add metadata to HLO.
  debug_info = jaxpr.debug_info
  del interpret, out_avals
  if grid_mapping.num_dynamic_grid_bounds:
    raise NotImplementedError(
        "dynamic grid bounds not supported in the Mosaic GPU backend"
    )

  if mesh is not None and not isinstance(mesh, gpu_core.Mesh):
    raise NotImplementedError(
        f"Mesh {mesh} is not supported by the Mosaic GPU backend"
    )

  if debug:
    print(f"\nThe kernel jaxpr for pallas_call {debug_info.func_src_info}:")
    print(jaxpr)
    print(f"The grid mapping for pallas_call {debug_info.func_src_info}:")
    print(grid_mapping)

  mgpu.dialect.register_dialect(ctx.module_context.context)

  if compiler_params is None:
    gpu_params = gpu_core.CompilerParams()
  else:
    assert isinstance(compiler_params, gpu_core.CompilerParams)
    gpu_params = compiler_params

  jax_mesh = None
  axis_context = ctx.module_context.axis_context
  if axis_context is not None:
    if isinstance(axis_context, sharding_impls.SPMDAxisContext):
      jax_mesh = axis_context.mesh

  lowering_result = lowering.lower_pipelined_jaxpr_to_module(
      grid_mapping,
      mesh,
      jax_mesh,
      jaxpr,
      gpu_params,
      cost_estimate,
      outer_traceback=ctx.traceback,
  )
  if debug:
    print(f"\nThe Mosaic GPU module for pallas_call {debug_info.func_src_info}:")
    print(lowering_result.module.operation)

  module = lowering_result.module
  new_avals_in = list(ctx.avals_in)
  new_avals_out = list(map(_as_shaped_array, lowering_result.new_out_shapes))
  scratch_args = ()
  if lowering_result.gmem_scratch_shapes:
    # The new_out_shapes contain the original outputs first, followed by the
    # GMEM scratch shapes, and optionally the profiler buffer.
    input_output_aliases += tuple(
        (len(ctx.avals_in) + i, len(ctx.avals_out) + i)
        for i in range(len(lowering_result.gmem_scratch_shapes))
    )
    # The GMEM scratch is an aliased kernel input/output.
    new_avals_in.extend(map(_as_shaped_array, lowering_result.gmem_scratch_shapes))
    # We guarantee zero-initialization of the GMEM scratch at the moment, which
    # is important for semaphores.
    def zero_init_gmem_scratch():
      return [jnp.zeros_like(s) for s in lowering_result.gmem_scratch_shapes]
    scratch_args = mlir.lower_fun(
        zero_init_gmem_scratch, multiple_results=True
    )(ctx.replace(avals_in=()))
  outs = mgpu.core._mosaic_gpu_lowering_rule(
      ctx.replace(avals_in=new_avals_in, avals_out=new_avals_out),
      *args, *scratch_args,
      module=module,
      out_types=lowering_result.new_out_shapes,
      inout_types=(),
      input_output_aliases=input_output_aliases,
      # False until we add get_barrier_semaphore() feature.
      use_custom_barrier=False,
  )
  if (prof_spec := lowering_result.profiler_spec) is not None:
    *outs, prof_buffer = outs
    out_file = os.path.join(
        prof_spec.dump_path,
        f"{mlir.sanitize_name(debug_info.func_name)}-{time.time_ns()}-trace.json",
    )
    def dump_profile(prof_buffer):
      assert prof_spec is not None  # pyrefly#40
      try:
        with open(out_file, "x") as f:
          prof_spec.dump(
              prof_buffer,
              f,
              grid=lowering_result.grid,
              block=lowering_result.block,
          )
      except FileExistsError:
        warnings.warn(
            f"Failed to dump profile for pallas_call {debug_info.func_src_info}, "
            f"profile already exists at {out_file}"
        )
    def do_callback(prof_buffer):
      jax.debug.callback(dump_profile, prof_buffer)
      return ()
    mlir.lower_fun(do_callback, multiple_results=True)(
        ctx.replace(avals_in=(new_avals_out[-1],)), prof_buffer
    )
  if lowering_result.gmem_scratch_shapes:  # Drop the GMEM scratch.
    outs = outs[:-len(lowering_result.gmem_scratch_shapes)]
  return outs


def pallas_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    jaxpr: jax_core.Jaxpr,
    interpret: bool,
    debug: bool,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: pallas_core.GridMapping,
    mesh: pallas_core.Mesh | None,
    compiler_params: pallas_core.CompilerParams | None,
    cost_estimate: pallas_core.CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: frozen_dict.FrozenDict[str, str] | None,
    name: str | None,
):
  del interpret, out_avals, cost_estimate, name
  debug_info = jaxpr.debug_info
  if grid_mapping.num_dynamic_grid_bounds:
    raise NotImplementedError(
        "dynamic grid bounds not supported in the Triton backend"
    )
  if grid_mapping.num_index_operands:
    raise NotImplementedError(
        "scalar prefetch not implemented in the Triton backend"
    )
  if mesh is not None:
    raise NotImplementedError("mesh is not supported in the Triton backend")

  [lowering_platform] = ctx.platforms or ctx.module_context.platforms

  if compiler_params is None:
    triton_params = triton_core.CompilerParams()
  else:
    assert isinstance(compiler_params, triton_core.CompilerParams)
    triton_params = compiler_params

  num_warps = 4 if triton_params.num_warps is None else triton_params.num_warps
  num_stages = triton_params.num_stages
  if num_stages is None:
    num_stages = 1 if lowering_platform == "rocm" else 3

  if debug:
    print(f"\nThe kernel jaxpr for pallas_call {debug_info.func_src_info}:")
    print(jaxpr)
    print(f"The grid mapping for pallas_call {debug_info.func_src_info}:")
    print(grid_mapping)

  try:
    gpu_device, *_ = jax.local_devices(backend="gpu")
  except RuntimeError:
    # GPU device is not available. Fall back to the minimum CC supported by Triton.
    # TODO(slebedev): Make the fallback CC configurable.
    arch_name = "9.0"
    compute_capability = 90
  else:
    arch_name = str(gpu_device.compute_capability)
    if lowering_platform == "rocm":
      compute_capability = 0
    else:
      compute_capability = int(arch_name.replace(".", ""))

  # Sanitize the name to conform to NVPTX requirements. We do this here
  # to avoid the need to fetch the new name from PTX post compilation.
  name = mlir.sanitize_name(debug_info.func_name)
  lowering_result = lowering.lower_jaxpr_to_triton_module(
      jaxpr, grid_mapping, lowering_platform, compute_capability or None,
      mlir_ctx=ctx.module_context
  )
  module_op = lowering_result.module.operation
  if debug:
    print(f"\nThe Triton module for pallas_call {debug_info.func_src_info}:")
    print(module_op.get_asm(enable_debug_info=True, pretty_debug_info=True))

  grid_x, grid_y, grid_z = normalize_grid(lowering_result.grid)
  buf = io.BytesIO()
  module_op.write_bytecode(buf)

  serialized_metadata = None
  if metadata is not None:
    serialized_metadata = json.dumps(dict(metadata))

  # TODO(b/394629193): Remove this once the minimum jaxlib version is >0.10.1.
  if jaxlib_version <= (0, 10, 2):
    out_types = [
      ir.RankedTensorType.get(bm.array_aval.shape,
                              mlir.dtype_to_ir_type(bm.array_aval.dtype))
      for bm in grid_mapping.block_mappings_output
    ]
    backend_config = dict(
        name=ir.StringAttr.get(name),
        ir=ir.StringAttr.get(buf.getvalue()),
        num_stages=mlir.i32_attr(num_stages),
        num_warps=mlir.i32_attr(num_warps),
        grid_x=mlir.i32_attr(grid_x),
        grid_y=mlir.i32_attr(grid_y),
        grid_z=mlir.i32_attr(grid_z),
        debug=ir.BoolAttr.get(debug),
    )
    if serialized_metadata is not None:
      # This field is unstable and may be removed in the future.
      backend_config["serialized_metadata"] = ir.StringAttr.get(
          serialized_metadata
      )
    return mlir.custom_call(
        call_target_name="__gpu$xla.gpu.triton",
        result_types=out_types,
        operands=in_nodes,
        backend_config=backend_config,
        api_version=4,
        operand_layouts=avals_to_layouts(ctx.avals_in),
        result_layouts=avals_to_layouts(ctx.avals_out),
        operand_output_aliases=dict(input_output_aliases),
    ).results

  compilation_result = triton.compile(
      lowering_platform,
      buf.getvalue(),
      arch_name,
      num_warps=num_warps,
      num_ctas=1,
      num_stages=num_stages,
  )
  kernel = triton_kernel_call_lib.TritonKernel(
      name,
      num_warps,
      1,
      compilation_result.smem_bytes,
      (
          compilation_result.hsaco_path
          if lowering_platform == "rocm"
          else compilation_result.asm
      ),
      module_op.get_asm(enable_debug_info=True, pretty_debug_info=True),
      compute_capability,
  )
  kernel_call = triton_kernel_call_lib.TritonKernelCall(
      kernel,
      grid_x,
      grid_y,
      grid_z,
      [triton_kernel_call_lib.create_array_parameter(0, 16)]
      * (len(ctx.avals_in) + len(ctx.avals_out)),
  )
  result_types, _ = mlir.ir_tree_registry.flatten([
      mlir.aval_to_ir_type(ctx.module_context, aval)
      for aval in ctx.avals_out
  ])
  return mlir.custom_call(
      call_target_name="triton_kernel_call_ffi",
      result_types=result_types,
      operands=in_nodes,
      backend_config=dict(
          name=ir.StringAttr.get(name),
          opaque=ir.StringAttr.get(
              zlib.compress(
                  kernel_call.to_proto(
                      name, (serialized_metadata or "").encode()
                  )
              )
          ),
      ),
      operand_layouts=avals_to_layouts(ctx.avals_in),
      result_layouts=avals_to_layouts(ctx.avals_out),
      operand_output_aliases=dict(input_output_aliases),
  ).results

