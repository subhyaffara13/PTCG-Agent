
def emit_pipeline(
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
):
  if any(g <= 0 for g in grid if isinstance(g, int)):
    raise ValueError(
        f"All elements in the grid must be strictly positive, but got {grid=}"
    )

  if not config.use_emit_pipeline_primitive.value:
    return _emit_pipeline(
        body,
        grid=grid,
        in_specs=in_specs,
        out_specs=out_specs,
        tiling=tiling,
        core_axis=core_axis,
        core_axis_name=core_axis_name,
        dimension_semantics=dimension_semantics,
        trace_scopes=trace_scopes,
        no_pipelining=no_pipelining,
        _explicit_indices=_explicit_indices,
    )

  in_specs = _normalize_specs(in_specs)
  out_specs = _normalize_specs(out_specs)
  in_specs_flat, _ = tree_util.tree_flatten(in_specs)
  out_specs_flat, _ = tree_util.tree_flatten(out_specs)

  def wrapped(*args, allocations=None):
    refs_flat, refs_tree = tracing_registry.flatten(args, is_transformed_ref)
    if allocations is not None:
      # TODO(rdyro): Add support for allocations.
      raise NotImplementedError("`allocations` are not yet supported.")
    else:
      local_in_specs = in_specs_flat
      local_out_specs = out_specs_flat

    num_inputs = len(local_in_specs)
    in_refs, out_refs = refs_flat[:num_inputs], refs_flat[num_inputs:]

    # Split the grid into static and dynamic parts the latter passed as args.
    in_avals = [_ref_to_value_aval(r) for r in in_refs]
    out_avals = [_ref_to_value_aval(r) for r in out_refs]

    core_axis_ = core_axis_name if core_axis is None else core_axis
    grid_, grid_offsets = _partition_grid(grid, core_axis_, dimension_semantics)
    dynamic_offset_tracers, static_grid_offsets = [], []
    for d in grid_offsets:
      if isinstance(d, (core.Tracer, jax.Array)):
        dynamic_offset_tracers.append(d)
        static_grid_offsets.append(pallas_core.DynamicGridDim())
      else:
        static_grid_offsets.append(d)

    grid_spec = pallas_core.GridSpec(
        grid=grid_, in_specs=local_in_specs, out_specs=local_out_specs)
    static_grid_spec, dynamic_bounds = (
        pallas_core.unzip_dynamic_grid_bounds(grid_spec))
    # TODO(rdyro): Move this primitive to pallas_core or vendor get_grid_mapping
    # here.
    _, in_tree = tracing_registry.flatten(tuple(in_refs), is_transformed_ref)
    _, out_tree = tracing_registry.flatten(tuple(out_refs), is_transformed_ref)
    kernel_args, grid_mapping = pallas_core.get_grid_mapping(
        static_grid_spec,
        in_avals,
        in_tree,
        [""] * len(in_avals),
        out_avals,
        out_tree,
        [""] * len(out_avals),
        allow_captured_consts=True,
    )
    # Trace the kernel body to a jaxpr.
    kernel_args = refs_tree.unflatten(kernel_args)
    flat_kernel_args, kernel_in_tree = tracing_registry.flatten(
        kernel_args, is_transformed_ref)
    # Ensure the get_grid_mapping didn't produce TransformedRefs for tracing.
    assert all(
        not isinstance(x, state.TransformedRef) for x in flat_kernel_args)

    with grid_mapping.trace_env():
      body_fun_dbg = api_util.debug_info(
          "emit_pipeline body", body, kernel_args, {})
      flat_body_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
          lu.wrap_init(body, debug_info=body_fun_dbg),
          kernel_in_tree
      )
      body_jaxpr, _, body_consts = pe.trace_to_jaxpr_dynamic(
        flat_body_fun, tuple(flat_kernel_args)
      )
      if out_tree_thunk().num_leaves != 0:
        raise ValueError("The emit_pipeline body function must return None.")

    all_index_map_consts = tuple(itertools.chain.from_iterable(
        bm.index_map_jaxpr.consts for bm in grid_mapping.block_mappings))

    args_flat, args_tree = tracing_registry.flatten(args)
    return emit_pipeline_p.bind(
        *all_index_map_consts,
        *dynamic_bounds,
        *dynamic_offset_tracers,
        *body_consts,
        *args_flat,
        body_consts_len=len(body_consts),
        body_jaxpr=body_jaxpr,
        grid_mapping=grid_mapping,
        tiling=tiling,
        core_axis=core_axis,
        core_axis_name=core_axis_name,
        args_tree=args_tree,
        dimension_semantics=dimension_semantics,
        trace_scopes=trace_scopes,
        no_pipelining=no_pipelining,
        _static_grid_offsets=tuple(static_grid_offsets),
        _num_extra_dynamic=len(dynamic_offset_tracers),
    )
  return wrapped


def emit_pipeline(
    body: Callable[..., T],
    *,
    grid: pallas_core.TupleGrid,
    in_specs: Sequence[pallas_core.BlockSpec] = (),
    out_specs: Sequence[pallas_core.BlockSpec] = (),
    max_concurrent_steps: int = 1,
    init_carry: T | None = None,
):
  r"""Creates a function to emit a manual pipeline within a Pallas kernel.

  Args:
    body: The pipeline body function, which is called with

      - ``indices``: Tuple of current loop indices.
      - ``*input_refs``: SMEM refs for inputs.
      - ``*output_refs``: SMEM refs for outputs.

      If ``init_carry`` is provided, ``body`` receives an additional argument
      ``carry`` -- the carry from the previous iteration. It must then return
      the next carry value.
    grid: The grid dimensions for the pipeline.
    in_specs: A sequence of :class:`~jax.experimental.pallas.BlockSpec`\s
      for inputs.
    out_specs: A sequence of :class:`~jax.experimental.pallas.BlockSpec`\s
      for outputs.
    max_concurrent_steps: Maximum concurrently active pipeline stages.
    init_carry: Optional initial carry. If provided, ``body`` handles
      carry-over state between iterations, and the pipeline returns the
      final carry.

  Returns:
    A function that, when called with GMEM input and output refs, executes the
    pipeline and returns the final carry value (if ``init_carry`` was used),
    otherwise it returns None.
  """

  if any(g <= 0 for g in grid if isinstance(g, int)):
    raise ValueError(
        f"All elements in the grid must be strictly positive, but got {grid=}"
    )

  in_specs = tuple(map(_downcast_spec, in_specs))
  out_specs = tuple(map(_downcast_spec, out_specs))
  for spec in in_specs:
    if isinstance(spec, gpu_core.BlockSpec) and spec.collective_axes:
      raise NotImplementedError(
          "BlockSpecs with collective_axes are not supported in emit_pipeline"
      )
  for spec in out_specs:
    if isinstance(spec, gpu_core.BlockSpec) and spec.collective_axes:
      raise ValueError("Output BlockSpecs cannot have collective_axes")
  # TODO(justinfu): Factor out common code between warp-specialized and
  # normal pipelines.
  delay_release_levels = sorted(
      {getattr(s, "delay_release", 0) for s in in_specs} or {0}
  )
  if delay_release_levels and max_concurrent_steps <= delay_release_levels[0]:
    raise ValueError(
        "max_concurrent_steps must be greater than all delay_release values,"
        f" but {max_concurrent_steps=} and {delay_release_levels=}."
    )

  num_steps = math.prod(grid)
  has_dynamic_grid = not isinstance(num_steps, int)
  # Convert the grid to int32 explicitly to avoid dtype promotion errors.
  grid = tuple(jnp.asarray(g, dtype=jnp.int32) for g in grid)

  # Shrink ``max_concurrent_steps`` if the total number of steps is lower to
  # reduce the size of the refs allocated in SMEM.
  if not has_dynamic_grid and max_concurrent_steps > num_steps:
    max_concurrent_steps = int(num_steps)

  def pipeline(*gmem_refs: state.AbstractRef):
    in_gmem_refs, out_gmem_refs = util.split_list(gmem_refs, [len(in_specs)])
    in_smem_refs, out_smem_refs = util.split_list(
        [
            gpu_core.SMEM(
                (max_concurrent_steps, *_get_block_shape(spec, ref.shape)),
                ref.dtype,
                transforms=tuple(
                    gpu_core.batch_transform(t, 1)
                    for t in getattr(spec, "transforms", ())
                ),
            )
            if _in_smem(spec)
            else None
            for spec, ref in zip(it.chain(in_specs, out_specs), gmem_refs)
        ],
        [len(in_specs)],
    )
    num_arrivals = sum(map(_in_smem, in_specs))
    return pl.run_scoped(
        functools.partial(
            scoped_pipeline,
            in_gmem_refs=in_gmem_refs,
            out_gmem_refs=out_gmem_refs,
        ),
        in_smem_refs=in_smem_refs,
        out_smem_refs=out_smem_refs,
        barrier_ref=None
        if num_arrivals == 0
        else gpu_core.Barrier(
            # TODO(slebedev): Change this to arrive only once.
            num_arrivals=num_arrivals,
            num_barriers=max_concurrent_steps,
        ),
    )

  def scoped_pipeline(
      *, in_gmem_refs, out_gmem_refs, in_smem_refs, out_smem_refs, barrier_ref
  ):
    in_brefs: Sequence[BufferedRef] = [
        BufferedRef(spec, _is_index_invariant(spec, grid), gmem_ref, smem_ref)
        for spec, gmem_ref, smem_ref in zip(
            in_specs, in_gmem_refs, in_smem_refs
        )
    ]
    out_brefs: Sequence[BufferedRef] = [
        BufferedRef(spec, _is_index_invariant(spec, grid), gmem_ref, smem_ref)
        for spec, gmem_ref, smem_ref in zip(
            out_specs, out_gmem_refs, out_smem_refs
        )
    ]

    # Initialize the pipeline.
    indices = (jnp.asarray(0, dtype=jnp.int32),) * len(grid)
    if has_dynamic_grid:
      prologue_steps = lax.min(max_concurrent_steps, num_steps)
    else:
      assert max_concurrent_steps <= num_steps
      prologue_steps = max_concurrent_steps

    def prologue(step, fetch_indices):
      for bref in in_brefs:
        bref.copy_in(step, fetch_indices, barrier_ref)
      return _inc_grid_by_1(fetch_indices, grid)
    jax.lax.fori_loop(0, prologue_steps, prologue, indices, unroll=not has_dynamic_grid)

    # This is true if any of the outputs need to be transferred inside the loop.
    smem_out_brefs = [bref for bref in out_brefs if _in_smem(bref.spec)]
    copies_out_in_loop = not all(bref.is_index_invariant for bref in smem_out_brefs)
    needs_epilogue = any(bref.is_index_invariant for bref in smem_out_brefs)

    # In the loop body, `max_concurrent_steps` may be larger than `num_steps` in
    # the dynamic grid case. This is fine, since in that case, we will never
    # need to fetch more data anyway.
    def loop_body(step, carry):
      slot = lax.rem(step, max_concurrent_steps)
      indices, fetch_index_levels, last_store_indices, prev_body_carry = carry

      if barrier_ref is not None:
        # Wait for the current GMEM->SMEM copy to complete, if any.
        gpu_primitives.barrier_wait(barrier_ref.at[slot])
      # Wait for the previous output SMEM->GMEM copy to complete.
      if copies_out_in_loop:
        gpu_primitives.wait_smem_to_gmem(
            max_concurrent_steps - 1, wait_read_only=True
        )

      next_body_carry = body(
          indices,
          *(
              bref.get_ref_for_slot(slot)
              for bref in it.chain(in_brefs, out_brefs)
          ),
          *(prev_body_carry,) if init_carry is not None else (),
      )

      if copies_out_in_loop:
        gpu_primitives.commit_smem()

      # Copy the output from SMEM to GMEM.
      new_store_indices = last_store_indices[:]
      for idx, bref in enumerate(out_brefs):
        if bref.is_index_invariant:
          assert last_store_indices[idx] is None
          continue
        assert bref.spec.index_map is not None
        new_store_indices[idx] = bref.spec.index_map(*indices)
        assert last_store_indices[idx] is not None
        are_same_slices = map(
            lambda old, new: old == new,
            last_store_indices[idx],
            new_store_indices[idx],
        )
        slices_changed = lax.bitwise_not(
            functools.reduce(lax.bitwise_and, are_same_slices)
        )
        is_last_step = step == num_steps - 1
        # TODO(apaszke,slebedev): This still diverges significantly from the
        # TPU semantics in that it will move on to the next SMEM output slice
        # even if it's not storing the previous one.
        bref.copy_out(
            slot,
            indices,
            predicate=lax.bitwise_or(slices_changed, is_last_step),
        )

      if copies_out_in_loop:
        gpu_primitives.commit_smem_to_gmem_group()

      for delay_release, fetch_indices in zip(
          delay_release_levels, fetch_index_levels
      ):
        fetch_step = step + (max_concurrent_steps - delay_release)
        fetch_slot = lax.rem(fetch_step, max_concurrent_steps)
        def do_fetch():
          for bref in in_brefs:
            if getattr(bref.spec, "delay_release", 0) == delay_release:
              bref.copy_in(fetch_slot, fetch_indices, barrier_ref)

        jax.lax.cond(
            lax.bitwise_and(step >= delay_release, fetch_step < num_steps),
            do_fetch,
            lambda: None,
        )

      next_fetch_indices_levels = [
          _inc_grid_by_1(fetch_indices, grid)
          for fetch_indices in fetch_index_levels
      ]
      return (
          _inc_grid_by_1(indices, grid),
          next_fetch_indices_levels,
          new_store_indices,
          next_body_carry if init_carry is not None else None,
      )

    fetch_index_levels = []
    for delay_release in delay_release_levels:
      fetch_indices = indices
      for _ in range(max_concurrent_steps - delay_release):
        fetch_indices = _inc_grid_by_1(fetch_indices, grid)
      fetch_index_levels.append(fetch_indices)

    # TODO(justinfu): Only store base pointer instead of all indices.
    last_store_indices = [
        None
        if bref.is_index_invariant
        # pyrefly: ignore[bad-argument-type]
        else (jnp.array(-1),) * len(bref.spec.block_shape)
        for bref in out_brefs
    ]
    last_indices, _, _, final_carry = lax.fori_loop(
        0,
        num_steps,
        loop_body,
        (indices, fetch_index_levels, last_store_indices, init_carry),
    )

    # Outputs invariant to the sequential axis are never written from inside the
    # loop. This is the only place where we store them.
    if not copies_out_in_loop and needs_epilogue:
      gpu_primitives.commit_smem()

    if needs_epilogue:
      last_slot = lax.rem(num_steps - 1, max_concurrent_steps)
      for bref in out_brefs:
        if bref.is_index_invariant:
          bref.copy_out(last_slot, last_indices, predicate=None)

      gpu_primitives.commit_smem_to_gmem_group()

    if smem_out_brefs:
      # Finalize the pipeline.
      gpu_primitives.wait_smem_to_gmem(0)
    return final_carry if init_carry is not None else None

  return pipeline

