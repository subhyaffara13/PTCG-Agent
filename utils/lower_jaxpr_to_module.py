
def lower_jaxpr_to_module(
    module_name: str,
    jaxpr: core.ClosedJaxpr,
    *,
    num_const_args: int,
    in_avals: Sequence[core.AbstractValue],
    ordered_effects: list[core.Effect],
    # See ModuleContext.get_backend() for backend and platforms usage.
    platforms: Sequence[str],
    backend: xc.Client | None,
    axis_context: AxisContext,
    donated_args: Sequence[bool],
    replicated_args: Sequence[bool] | None = None,
    arg_shardings: Sequence[JSharding | None] | None = None,
    result_shardings: Sequence[JSharding | None] | None = None,
    in_layouts: Sequence[Layout | None | AutoLayoutSingleton] | None = None,
    out_layouts: Sequence[Layout | None | AutoLayoutSingleton] | None = None,
    arg_names: Sequence[str] | None = None,
    result_names: Sequence[str] | None = None,
    num_partitions: int = 1,
    all_default_mem_kind: bool = True,
    input_output_aliases: None | tuple[int | None, ...] = None,
    propagated_out_mem_kinds: tuple[None | str, ...] | None = None,
    lowering_parameters: LoweringParameters,
) -> LoweringResult:
  """Lowers a top-level jaxpr to an MLIR module.

  Handles the quirks of the argument/return value passing conventions of the
  runtime.
  The inputs already account for the constant arguments.
  See https://docs.jax.dev/en/latest/internals/constants.html
  """
  util.test_event("lower_jaxpr_to_module")
  platforms = tuple(map(xb.canonicalize_platform, platforms))

  sharded_in_avals = (in_avals if arg_shardings is None else
                      map(sharded_aval, in_avals, arg_shardings))
  sharded_out_avals = (jaxpr.out_avals if result_shardings is None else
                       map(sharded_aval, jaxpr.out_avals, result_shardings))
  if all_default_mem_kind:
    arg_memory_kinds = None
    result_memory_kinds = None
  else:
    arg_memory_kinds = (map(_get_mem_kind, arg_shardings)
                        if arg_shardings is not None else None)
    result_memory_kinds = (map(_get_mem_kind, result_shardings)
                          if result_shardings is not None else None)

  # TODO(yashkatariya): Simplify the donation logic.
  xla_donated_args = None
  platforms_with_donation = [p for p in platforms
                             if p in _platforms_with_donation]
  if platforms_with_donation:
    if len(platforms_with_donation) != len(platforms) and (
        xla_donated_args or any(donated_args)):
      raise NotImplementedError(
        "In multi-platform lowering either all or no lowering platforms "
        f"should support donation. Lowering for {platforms} of which "
        f"only {platforms_with_donation} support donation")
    input_output_aliases, donated_args, xla_donated_args = _set_up_aliases(
        input_output_aliases, sharded_in_avals, sharded_out_avals, donated_args,
        arg_memory_kinds, result_memory_kinds, in_layouts, out_layouts,
        result_shardings if num_partitions > 1 else None)
    if (num_partitions > 1 and
        (result_shardings is None or
         any(s is None or contains_unconstrained(s) for s in result_shardings))):
      if xla_donated_args is None:
        xla_donated_args = [False] * len(donated_args)
      for input_id in range(len(donated_args)):
        if donated_args[input_id]:
          xla_donated_args[input_id] = True
          donated_args[input_id] = False
  if any(donated_args):
    unused_donations = [str(a) for a, d in zip(sharded_in_avals, donated_args) if d]
    msg = "See an explanation at https://docs.jax.dev/en/latest/faq.html#buffer-donation."
    if not platforms_with_donation:
      msg = f"Donation is not implemented for {platforms}.\n{msg}"
    if unused_donations:
      warnings.warn("Some donated buffers were not usable:"
                    f" {', '.join(unused_donations)}.\n{msg}")
  # Delete donated_args by default here, since it's not needed beyond this point
  del donated_args

  unlowerable_effects = effects_lib.lowerable_effects.filter_not_in(
      jaxpr.effects)
  if unlowerable_effects:
    raise ValueError(f'Cannot lower jaxpr with effects: {jaxpr.effects}')

  # HLO channels need to start at 1. We reserve 1 for collectives.
  channel_iter = itertools.count(COLLECTIVE_CHANNEL_ID + 1)
  # Create a keepalives list that will be mutated during the lowering.
  keepalives: list[Any] = []
  host_callbacks: list[Any] = []
  # Find the dimension variables
  all_dim_poly = [d for aval in sharded_in_avals if hasattr(aval, "shape")
                  for d in aval.shape if not core.is_constant_dim(d)]
  dim_vars = tuple(sorted(functools.reduce(lambda acc, new: acc.union(new._get_vars()),
                                           all_dim_poly, set())))


  ctx = ModuleContext(backend=backend,
                      platforms=platforms, axis_context=axis_context,
                      keepalives=keepalives,
                      channel_iterator=channel_iter,
                      host_callbacks=host_callbacks,
                      lowering_parameters=lowering_parameters,
                      shape_poly_state=ShapePolyLoweringState(dim_vars, platforms),
                      all_default_mem_kind=all_default_mem_kind)
  with ctx.context, ir.Location.unknown(ctx.context):
    # Remove module name characters that XLA would alter. This ensures that
    # XLA computation preserves the module name.
    attrs = ctx.module.operation.attributes
    attrs["sym_name"] = ir.StringAttr.get(
        sanitize_name(module_name).rstrip("_"))
    attrs["mhlo.num_replicas"] = i32_attr(1)
    attrs["mhlo.num_partitions"] = i32_attr(num_partitions)
    lower_jaxpr_to_fun(
        ctx, module_name, jaxpr, ordered_effects,
        num_const_args=num_const_args,
        main_function=True,
        replicated_args=replicated_args,
        in_avals=in_avals,
        arg_shardings=arg_shardings,
        result_shardings=result_shardings,
        input_output_aliases=input_output_aliases,
        xla_donated_args=xla_donated_args,
        arg_names=arg_names,
        result_names=result_names,
        arg_memory_kinds=arg_memory_kinds,
        result_memory_kinds=result_memory_kinds,
        arg_layouts=in_layouts,
        result_layouts=out_layouts,
        propagated_out_mem_kinds=propagated_out_mem_kinds)

  try:
    if not ctx.module.operation.verify():
      raise ValueError(
          "Cannot lower jaxpr with verifier errors. " +
          dump_module_message(ctx.module, "verification"))
  except ir.MLIRError as e:
    msg_lines = ["Cannot lower jaxpr with verifier errors:"]
    def emit_diagnostic_info(d):
      msg_lines.append(f"\t{d.message}")
      msg_lines.append(f"\t\tat {d.location}")
      for n in d.notes:
        emit_diagnostic_info(n)
    for d in e.error_diagnostics:
      emit_diagnostic_info(d)
    raise ValueError("\n".join(msg_lines) + "\n" +
                     dump_module_message(ctx.module, "verification")) from e

  with ctx.context:
    if config.use_shardy_partitioner.value:
      pipeline = passmanager.PassManager.parse(
          'builtin.module(sdy-lift-inlined-meshes)')
      pipeline.run(ctx.module.operation)

  util.test_event("mlir.collect_lowered_jaxprs", jaxpr, ctx.module)
  return LoweringResult(ctx.module, ctx.keepalives, ctx.host_callbacks,
                        ctx.shape_poly_state)


def lower_jaxpr_to_module(
    jax_mesh: mesh_lib.Mesh | None,
    axis_names: _AxisNames,
    grid: tuple[int, ...],
    block: tuple[int, int, int],
    cluster: tuple[int, ...],
    in_shapes: Sequence[jax_core.ShapedArray],
    out_shapes: Sequence[jax_core.ShapedArray],
    jaxpr: jax_core.Jaxpr,
    params: gpu_core.CompilerParams,
    consts=(),
    outer_traceback: xc.Traceback | None = None,
) -> LoweringResult:
  debug_info = jaxpr.debug_info
  approx_math = params.approx_math
  lowering_semantics = params.lowering_semantics

  if len(cluster) < 3:
    cluster = (1,) * (3 - len(cluster)) + cluster
  else:
    assert len(cluster) == 3

  if len(grid) <= 3:
    squashed_dims = ()
    parallel_grid = (1,) * (3 - len(grid)) + grid
  else:
    # If we have >3 parallel dimensions, we flatten all but the minormost 2 dims.
    # Ex: (2, 3, 4, 5) -> (6, 4, 5)
    squashed_dims = grid[:-2]
    parallel_grid = (math.prod(grid[:-2]), *grid[-2:])

  # We reverse the order because Pallas prefers row-major iteration while the
  # CUDA runtime prefers column-major iteration.
  parallel_grid = parallel_grid[::-1]
  cluster = cluster[::-1]
  squashed_dims = squashed_dims[::-1]
  axis_names = axis_names.reverse()

  rs = _estimate_resources(
      ResourceEstimatorContext(
          reduction_scratch_bytes=params.reduction_scratch_bytes,
          axis_names=axis_names, lowering_semantics=lowering_semantics
      ),
      jaxpr,
  )

  def body(launch_ctx: mgpu.LaunchContext, *buffers: Any):
    *buffers_gmem, (
        runtime_smem,
        runtime_barriers,
        runtime_tmem,
    ) = buffers
    num_input_buffers = (len(in_shapes) +
                         len(rs.scoped_gmem_semaphores))
    input_buffers_gmem = buffers_gmem[:num_input_buffers]
    output_buffers_gmem = buffers_gmem[num_input_buffers:]

    scoped_gmem_semaphores = {}
    # pyrefly: ignore[no-matching-overload]
    for collective_axes in sorted(rs.scoped_gmem_semaphores, reverse=True):
      num_sems = rs.scoped_gmem_semaphores[collective_axes]
      # Extract the semaphores local to the current scope.
      index = ir.IndexType.get()
      # TODO(justinfu): Compute scope_idx for general collective_axes.
      # scope_idx computes axis_index(all_axes - collective_axes)
      if _is_block_local_scope(collective_axes, axis_names):
        scope_idx = arith_dialect.index_castui(index, mgpu_utils.block_idx())
      elif _is_global_scope(collective_axes, axis_names):
        scope_idx = _as_index(0)
      else:
        raise NotImplementedError(
            f"Unimplemented scope for semaphores: {collective_axes=}")
      scoped_gmem_semaphores[collective_axes] = mgpu.memref_slice(
          output_buffers_gmem[-1],
          mgpu.ds(
              arith_dialect.muli(
                  scope_idx, arith_dialect.constant(index, num_sems)
              ),
              num_sems,
          ),
      )
      # The semaphore buffer is an aliased input/output, so we need to skip it
      # in both the inputs and outputs.
      input_buffers_gmem = input_buffers_gmem[:-1]
      output_buffers_gmem = output_buffers_gmem[:-1]
    buffers_gmem = [*input_buffers_gmem, *output_buffers_gmem]

    grouped_barriers: MutableMapping[AnyBarrier, MutableSequence[AnyBarrierRef]]
    grouped_barriers = collections.defaultdict(list)
    for barrier, barrier_ref in zip(rs.barriers, runtime_barriers):
      grouped_barriers[barrier].append(barrier_ref)
    if runtime_tmem is not None:
      if lowering_semantics == mgpu.LoweringSemantics.Lane:
        tmem_cols = math.prod(runtime_tmem.shape) // tcgen05.TMEM_ROWS
        tmem_base = runtime_tmem.address
      else:
        tmem_cols = math.prod(runtime_tmem.type.shape) // tcgen05.TMEM_ROWS
        tmem_base = runtime_tmem
    else:
      tmem_cols = 0
      tmem_base = None

    single_wg_lane_predicate = mgpu.single_thread_predicate(
        scope=mgpu.ThreadSubset.WARPGROUP)
    single_warp_lane_predicate = mgpu.single_thread_predicate(
        scope=mgpu.ThreadSubset.WARP)

    module_ctx = ModuleContext(
        mlir.sanitize_name(debug_info.func_name),
        axis_names,
        [
            _program_id(axis, squashed_dims, len(grid))
            for axis in range(len(grid))
        ],
        approx_math,
        single_wg_lane_predicate,
        single_warp_lane_predicate,
        smem_requested_bytes=math.prod(ir.MemRefType(runtime_smem.type).shape),
        smem_used_bytes=0,
        tmem_requested_cols=tmem_cols,
        tmem_used_cols=0,
        tmem_base=tmem_base,
        scoped_gmem_used_semaphores={k: 0 for k in scoped_gmem_semaphores},
        scoped_gmem_semaphore_base_ptr=scoped_gmem_semaphores,
        runtime_barriers=grouped_barriers,
        name_stack=source_info_util.NameStack(),
        traceback_caches=mlir.TracebackCaches(),
        squashed_dims=squashed_dims,
        lowering_semantics=lowering_semantics,
        primitive_semantics=gpu_core.PrimitiveSemantics.Warpgroup,
        mesh_info=pallas_utils.MeshInfo.from_mesh(jax_mesh)
        if jax_mesh is not None
        else None,
        auto_barriers=not params.unsafe_no_auto_barriers,
        reduction_scratch_bytes=params.reduction_scratch_bytes,
        outer_traceback=outer_traceback,
    )
    del runtime_smem, grouped_barriers, runtime_barriers
    _ = lower_jaxpr_to_mosaic_gpu(
        module_ctx, launch_ctx, jaxpr, buffers_gmem, consts
    )

  scratch_buffers: list[Any] = [
      jax.ShapeDtypeStruct(shape=[rs.smem_scratch_bytes], dtype=np.int8),
      rs.barriers,
  ]
  if rs.tmem_scratch_cols > 0 and rs.tmem_collective_scratch_cols > 0:
    raise ValueError(
        "Can't mix collective and non-collective TMEM allocations within the"
        " same kernel."
    )
  tmem_scratch_cols = rs.tmem_scratch_cols + rs.tmem_collective_scratch_cols
  if tmem_scratch_cols > 0:
    scratch_buffers.append(
        mgpu.TMEM(
            shape=(tcgen05.TMEM_ROWS, tmem_scratch_cols),
            dtype=np.int32,
            collective=rs.tmem_collective_scratch_cols > 0,
        ),
    )
  else:
    scratch_buffers.append(None)

  prof_spec = None
  if params.profile_space:
    # Each range is 2 events, each event costs 2 entries.
    if params.profile_trace_scope == gpu_core.TraceScope.WARP:
      trace_scope = mgpu.ThreadSubset.WARP
    elif params.profile_trace_scope == gpu_core.TraceScope.WARPGROUP:
      trace_scope = mgpu.ThreadSubset.WARPGROUP
    else:
      raise ValueError(f"Unsupported trace scope: {params.profile_trace_scope}")
    prof_spec = mgpu_profiler.ProfilerSpec(
        params.profile_space * 2 * 2, dump_path=params.profile_dir,
        trace_scope=trace_scope
    )
  cuda_grid = tuple(map(operator.mul, parallel_grid, cluster))

  scoped_semaphores_shape = []
  for collective_axes in sorted(rs.scoped_gmem_semaphores):  # pyrefly: ignore[bad-specialization]
    num_sems = rs.scoped_gmem_semaphores[collective_axes]
    # TODO(justinfu): Compute axis_size for general collective_axes.
    # axis_size computes axis_size(all_axes - collective_axes)
    if _is_block_local_scope(collective_axes, axis_names):
      axis_size = math.prod(cuda_grid)
    elif _is_global_scope(collective_axes, axis_names):
      axis_size = 1
    else:
      raise NotImplementedError(
          f"Unimplemented scope for semaphores: {collective_axes=}")
    scoped_semaphores_shape.append(
        jax.ShapeDtypeStruct(
            shape=(axis_size * num_sems,), dtype=np.int32
        ),
    )
  scoped_semaphores_shape = tuple(scoped_semaphores_shape)

  if outer_traceback is not None:
    frame = source_info_util.user_frame(outer_traceback)
    if frame is not None:
      base_loc = ir.Location.file(
          mlir.get_canonical_source_file(
              frame.file_name, mlir.TracebackCaches()
          ),
          frame.start_line,
          frame.start_column,
      )
    else:
      base_loc = None
  else:
    base_loc = None

  # NOTE: new_out_shapes has out_shapes, then semaphores_shape and
  # optionally the profiler buffer.
  module, new_out_shapes, _, launch_ctx = mgpu_core._lower_as_gpu_kernel(
      body,
      grid=cuda_grid,
      cluster=cast(tuple[int, int, int], cluster),
      block=block,
      in_shapes=(*in_shapes, *scoped_semaphores_shape),
      out_shape=(*out_shapes, *scoped_semaphores_shape),
      inout_shape=(),
      smem_scratch_shape=scratch_buffers,
      lowering_semantics=lowering_semantics,
      module_name=mlir.sanitize_name(debug_info.func_name),
      kernel_name=mlir.sanitize_name(debug_info.func_name),
      prof_spec=prof_spec,
      jax_mesh=jax_mesh,
      base_loc=base_loc,
  )

  if lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    # We need to run a pass that removes dead-code for which layout inference
    # does not work.
    pm = mlir.passmanager.PassManager.parse("builtin.module(canonicalize,cse)", module.context)
    pm.run(module.operation)

    # Run Python lowering passes. The remaining passes will be run in C++ in
    # jax/jaxlib/mosaic/gpu/custom_call.cc
    mgpu.infer_layout(module, arch=mgpu_core._infer_arch())
    mgpu.lower_mgpu_dialect(
        module, launch_ctx, auto_barriers=not params.unsafe_no_auto_barriers
    )

  launch_ctx.scratch.finalize_size()

  return LoweringResult(
      module, cuda_grid, block, new_out_shapes, prof_spec,
      scoped_semaphores_shape,
  )

