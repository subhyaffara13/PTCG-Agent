
def lower_pipelined_jaxpr_to_module(
    grid_mapping: pallas_core.GridMapping,
    gpu_mesh: gpu_core.Mesh | None,
    jax_mesh: mesh_lib.Mesh | None,
    jaxpr: jax_core.Jaxpr,
    params: gpu_core.CompilerParams,
    cost_estimate: pallas_core.CostEstimate | None,
    outer_traceback: xc.Traceback | None = None,
) -> LoweringResult:
  del cost_estimate  # Unused.

  assert len(jaxpr.outvars) == 0
  assert not grid_mapping.vmapped_dims
  if grid_mapping.num_dynamic_grid_bounds:
    raise NotImplementedError(
        "Dynamic grid bounds not supported in the Mosaic GPU lowering."
    )
  if grid_mapping.num_index_operands:
    raise NotImplementedError(
        "Scalar prefetch not supported in Mosaic GPU lowering."
    )

  block_mappings = grid_mapping.block_mappings
  _check_block_mappings(block_mappings, jaxpr.debug_info)
  in_block_mappings, out_block_mappings = util.split_list(
      block_mappings, [grid_mapping.num_inputs]
  )

  grid: Sequence[int]
  if gpu_mesh:
    assert isinstance(gpu_mesh, gpu_core.Mesh)
    block = (128 * (gpu_mesh.num_threads or 1), 1, 1)
    grid = gpu_mesh.grid
    thread_axis = (
        gpu_mesh.thread_name if gpu_mesh.thread_name is not None else ()
    )
  else:
    block = (128, 1, 1)
    grid = cast(Sequence[int], grid_mapping.grid)
    thread_axis = ()

  if params.dimension_semantics is None:
    which_parallel = [True] * len(grid)
  else:
    assert len(params.dimension_semantics) == len(grid)
    which_parallel = [ds == "parallel" for ds in params.dimension_semantics]

  sequential_grid = tuple(
      d for axis, d in enumerate(grid) if not which_parallel[axis]
  )
  parallel_grid = tuple(
      d for axis, d in enumerate(grid) if which_parallel[axis]
  )

  from jax._src.pallas.mosaic_gpu import pipeline  # pyrefly: ignore[missing-module-attribute]

  def ref_for_aval(aval: ShapedAbstractValue):
    if isinstance(aval, gpu_core.WGMMAAbstractAccumulatorRef):
      return gpu_core.WGMMAAccumulatorRef(aval.shape, aval.dtype)
    elif isinstance(aval, gpu_core.AbstractTMEMRef):
      return gpu_core.GPUMemoryRef(
          jax_core.ShapedArray(aval.shape, aval.dtype), gpu_core.TMEM,
          transforms=(), layout=aval.layout, collective=aval.collective,
      )
    elif isinstance(aval, state_types.AbstractRef):
      if (memory_space := aval.memory_space) is pallas_core.MemorySpace.DEFAULT:
        memory_space = gpu_core.GMEM
      return pallas_core.MemoryRef(jax_core.ShapedArray(aval.shape, aval.dtype),
                                   memory_space)
    else:
      return gpu_core.SMEM(aval.shape, aval.dtype)

  def pipeline_fn(*refs):
    primitives.run_scoped(
        functools.partial(scoped_pipeline_fn, *refs),
        scratch_refs=[
            ref_for_aval(cast(ShapedAbstractValue, v.aval))
            for v in jaxpr.invars[grid_mapping.slice_scratch_ops]
        ],
        collective_axes=thread_axis,  # scratch_refs are shared across threads
    )
    return ()  # ``wrap_init`` does not support functions returning None.

  def scoped_pipeline_fn(*refs, scratch_refs):
    def body_fn(indices, *refs):
      program_ids_template = util.merge_lists(
          which_parallel, indices, [None] * sum(which_parallel)
      )
      assert len(refs) + len(scratch_refs) == len(jaxpr.invars)
      return primitives._jaxpr_call(
          jaxpr, *refs, *scratch_refs, program_ids=program_ids_template
      )

    return pipeline.emit_pipeline(
        body_fn,
        grid=sequential_grid,
        in_specs=[
            _block_spec_from_block_mapping(bm, which_parallel)
            for bm in in_block_mappings
        ],
        out_specs=[
            _block_spec_from_block_mapping(bm, which_parallel)
            for bm in out_block_mappings
        ],
        max_concurrent_steps=params.max_concurrent_steps,
    )(*refs)

  with grid_mapping.trace_env():
    new_jaxpr, _, new_consts = pe.trace_to_jaxpr_dynamic(
        lu.wrap_init(pipeline_fn, debug_info=jaxpr.debug_info.with_unknown_names()),
        [
            gpu_core.GMEM(
                bm.array_aval.shape, bm.array_aval.dtype
            ).get_ref_aval()
            for bm in block_mappings
        ],
    )
    assert not new_consts

  axis_names = (
      _AxisNames(gpu_mesh.grid_names, gpu_mesh.cluster_names, gpu_mesh.thread_name)
      if gpu_mesh is not None
      else _AxisNames(grid_mapping.grid_names or ())
  )
  with grid_mapping.trace_env():
    return lower_jaxpr_to_module(
        jax_mesh,
        axis_names,
        parallel_grid,
        block,
        tuple(gpu_mesh.cluster) if gpu_mesh is not None else (),
        [bm.array_aval for bm in in_block_mappings],
        [bm.array_aval for bm in out_block_mappings],
        new_jaxpr,
        params,
        new_consts,
        outer_traceback=outer_traceback,
    )

