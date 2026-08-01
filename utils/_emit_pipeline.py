
def _emit_pipeline(
    body,
    *,
    grid: tuple[int | jax.Array, ...],
    in_specs=(),
    out_specs=(),
    tiling: Tiling | None = None,
    core_axis: tuple[int, ...] | int | None = None,
    core_axis_name: tuple[str, ...] | str | None = None,
    dimension_semantics: tuple[GridDimensionSemantics, ...] | None = None,
    trace_scopes: bool = True,
    no_pipelining: bool = False,
    _explicit_indices: bool = False,
    _grid_offsets: tuple[int | jax.Array, ...] | None = None,
):
  """Creates a function to emit a manual pallas pipeline.

  This has the same semantics as pallas_call but is meant to be called inside
  pallas_call for nesting grids. This is useful when you need to have separate
  windowing strategies for communication and computation.

  Args:
    body: pallas kernel to set up pipeline for.
    grid: a pallas grid definition.
    in_specs: input pallas block specs
    out_specs: output pallas block specs
    tiling: optional tiling to assume for the refs.
    core_axis: optional int or tuple of int, indicates whether or not to
      partition the grid along the core axis.
    core_axis_name: optional str or tuple of str, indicates whether or not to
      partition the grid along the core axis.
    dimension_semantics: optional tuple of GridDimensionSemantics (e.g. PARALLEL
      or ARBITRARY).
    trace_scopes: optional bool, indicates whether to annotate each region in
      the pipeline using named_scope.
    no_pipelining: If True, turns off pipelining and all copies will be made
      synchronous. This is useful for debugging multiple-buffering related bugs.
    _explicit_indices: If True, the body will receive the iteration indices as
      its first argument. This parameter is meant for internal use only.
    _grid_offsets: If provided, the grid partitioning offset indices and sizes
      are already precomputed and the scheduler will use these values directly.
      Internal use only.
  """

  if any(not isinstance(d, (int, jax.Array)) for d in grid):
    grid_types = tuple(type(d) for d in grid)
    raise ValueError(
        f"Grid must consist of Python integers and JAX Arrays: {grid_types}"
    )
  if not (core_axis is None or core_axis_name is None):
    raise ValueError("core_axis and core_axis_name cannot both be provided.")
  if _grid_offsets is None:
    core_axis_ = core_axis_name if core_axis is None else core_axis
    grid, grid_offsets = _partition_grid(grid, core_axis_, dimension_semantics)
  else:
    grid_offsets = _grid_offsets

  num_steps = math.prod(grid)
  in_specs = _normalize_specs(in_specs)
  out_specs = _normalize_specs(out_specs)
  get_buffer_count = lambda spec: (spec.pipeline_mode.buffer_count if
    (spec is not None and spec.pipeline_mode is not None) else 2)
  flattened_specs = jax.tree.leaves((in_specs, out_specs))
  max_buffer_count = max((2, *map(get_buffer_count, flattened_specs)))

  def pipeline(
      *refs: Any,
      scratches=None,
      allocations=None,
      body_prologue=None,
  ):
    """
    Run the pipeline.

    Args:
      *ref_args: a list of pallas refs (or more generally a list of pytrees of
        pallas refs)
      scratches: scratch buffers for the inner kernel
      allocations: a list of BufferedRefs, one corresponding to each ref
      body_prologue: For running code within the grid environment before the
        body is run. Useful for updating manual refs.
    """
    if scratches is None:
      scratches = ()
    if allocations is None:
      # run with inline scoped allocations
      return primitives.run_scoped(
          lambda allocations: pipeline(
              *refs,
              scratches=scratches,
              allocations=allocations,
          ),
          _make_pipeline_allocations(
              *refs,
              in_specs=in_specs,
              out_specs=out_specs,
              grid=grid,
              tiling=tiling,
          )
      )
    if isinstance(allocations, list):
      allocations = tuple(allocations)

    def make_scheduler(step, indices):
      return Scheduler(
          step,
          indices,
          grid,
          grid_offsets=grid_offsets,
          num_stages=max_buffer_count,
          trace_scopes=trace_scopes,
          _explicit_indices=_explicit_indices,
      )

    def loop_body(step, carry):
      unaliased_brefs, indices = carry
      indices = _filter_indices(indices, grid)
      scheduler = make_scheduler(step, indices)
      with scheduler.grid_env():
        # prepare any local VMEM aliases
        brefs = map_brefs(scheduler.alias_local_refs, unaliased_brefs, refs)
        # loop input handling phase
        brefs = map_brefs(scheduler.copy_in, brefs, refs)
        brefs = map_brefs(scheduler.wait_in, brefs, refs)

        # run the kernel!
        if body_prologue is not None:
          body_prologue()
        current_refs = map_brefs(lambda x: x.current_ref, brefs)
        with scheduler._named_scope("ep_run_kernel"):
          if _explicit_indices:
            body(scheduler.indices, *current_refs, *scratches)
          else:
            body(*current_refs, *scratches)

        # loop output handling phase
        brefs = map_brefs(scheduler.copy_out, brefs, refs)
        brefs = map_brefs(scheduler.wait_out, brefs, refs)

        brefs = map_brefs(scheduler.advance_slots, brefs)
        # Unbind window_refs for VMEM-backed buffers. Without this
        # we will be returning TransformedRefs which are not valid
        # JAX types.
        brefs = map_brefs(scheduler.unalias_local_refs, brefs)
      return brefs, _next_index(indices, grid)

    if no_pipelining:
      # Debugging mode where all copies are synchronous.
      initial_indices = (0,) * len(grid)
      brefs = map_brefs(lambda bref: bref.initialize_slots(), allocations)

      @functools.partial(
          jax.lax.fori_loop,
          0,
          num_steps,
          init_val=(brefs, initial_indices),
      )
      def _loop_body(step, carry):
        brefs, indices = carry
        indices = _filter_indices(indices, grid)
        scheduler = make_scheduler(step, indices)
        with scheduler.grid_env():
          # prepare any local VMEM aliases
          brefs = map_brefs(scheduler.alias_local_refs, brefs, refs)
          # loop input handling phase
          copy_in = lambda bref, ref: sync_copy(ref, bref, indices)
          map_inputs(copy_in, brefs, refs)
          # run the kernel!
          if body_prologue is not None:
            body_prologue()
          current_refs = map_brefs(lambda x: x.current_ref, brefs)
          with scheduler._named_scope("ep_run_kernel"):
            if _explicit_indices:
              body(scheduler.indices, *current_refs, *scratches)
            else:
              body(*current_refs, *scratches)
          # loop output handling phase
          copy_out = lambda bref, ref: sync_copy(bref, ref, indices)
          map_outputs(copy_out, brefs, refs)
        brefs = map_brefs(scheduler.unalias_local_refs, brefs)
        return brefs, _next_index(indices, grid)
    else:
      @when(num_steps > 0)
      def _():
        # pipeline prologue
        initial_indices = (0,) * len(grid)
        scheduler = make_scheduler(0, initial_indices)
        brefs = map_brefs(lambda bref: bref.initialize_slots(), allocations)
        def _sync_copy_in(bref, ref):
          if bref.is_trivial_windowing and bref.window_ref is not None:
            sync_copy(ref, bref, initial_indices)

        map_inputs(_sync_copy_in, brefs, refs)
        with scheduler.grid_env():
          # We issue num_stages-1 prefetch copies per buffer.
          # We iterate over steps in the outer loop because we want to
          # queue all iteration 0 prefetches before iteration 1, and so on.
          for step in range(scheduler.num_stages - 1):
            brefs = map_brefs(functools.partial(
                scheduler.initialize_step, step=step),
                brefs, refs)

        # pipeline loop
        brefs, next_indices = lax.fori_loop(
            0, num_steps, loop_body, (brefs, initial_indices)
        )

        # pipeline epilogue
        final_indices = _prev_index(next_indices, grid)
        scheduler = make_scheduler(num_steps - 1, final_indices)
        with scheduler.grid_env():
          map_brefs(scheduler.finalize, brefs, refs)

        def _sync_copy_out(bref, ref):
          if bref.is_trivial_windowing and bref.window_ref is not None:
            sync_copy(bref, ref, initial_indices)

        map_outputs(_sync_copy_out, brefs, refs)

  return pipeline

