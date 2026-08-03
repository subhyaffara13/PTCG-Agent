import functools
from typing import Any, Callable
import math


def emit_pipeline_warp_specialized(
    body: Callable[..., None],
    *,
    grid: pallas_core.TupleGrid,
    memory_registers: int,
    in_specs: BlockSpecPytree = (),
    out_specs: BlockSpecPytree = (),
    max_concurrent_steps: int = 2,
    wg_axis: str,
    num_compute_wgs: int,
    pipeline_state: jax.Array | PipelinePipeline | None = None,
    manual_consumed_barriers: bool = False,
    compute_context: ComputeContext | None = None,
    memory_thread_idx: int | None = None,
) -> WarpSpecializedPipeline:
  """Creates a function to emit a warp-specialized pipeline.

  The ``body`` function should have the following signature (without carry).
  ``consumed_barriers`` is an optional argument that is only passed if the
  ``manual_consumed_barriers`` argument is True::

    def body(indices, *input_refs, *output_refs, *consumed_barriers) -> None:

  or with a carries enabled (enabled via the ``compute_context`` argument),
  where the body returns the next carry::

    def body(
        indices, *input_refs, *output_refs, *consumed_barriers, carry
    ) -> Carry:

  When ``manual_consumed_barriers`` is True, the user must arrive on all the
  consumed barriers from all compute warpgroups at each pipeline step.

  Args:
    body: The pipeline body.
    grid: The grid to use for the pipeline.
    memory_registers: The number of registers to reserve for the memory thread.
      For H100 GPUs, 40 is a reasonable value.
    in_specs: The block specs for the inputs.
    out_specs: The block specs for the outputs.
    max_concurrent_steps: The maximum number of sequential stages that are
      active concurrently. Defaults to 2.
    wg_axis: The axis name for the warp group axis.
    num_compute_wgs: The number of compute warpgroups
    manual_consumed_barriers: If True, consumed barriers will be
      passed into the body function after the output refs. There will be one
      barrier per input and will be passed in the same order.
    compute_context: If specified, enables carries in the pipeline and allows
      a user-specified prologue/epilogue that is only executed in the compute
      thread. The signature of the pipeline body function will be modified
      such that the last argument will be the current carry and it must
      return the next carry.
      The compute_context itself should follow the signature of `ComputeContext`
      and take a pipeline function as its sole argument. Calling the
      pipeline with the initial carry will run the pipeline and return the
      final carry.
    memory_thread_idx: The index of the memory thread. If not specified,
      defaults to the last thread.
    pipeline_state: If multiple pipelines that have almost the same parameters
      (only in/out_specs and body can differ) are going to be evaluated
      in sequence, this argument can be used to avoid pipeline bubbles between
      their invocations. The first pipeline in the sequence should use the
      ``START`` state, followed by an arbitrary number of ``STEADY`` states,
      followed by a single ``STOP`` state. Note that until the pipeline with
      ``STOP`` is done, the memory thread will not wait for the compute threads
      to complete and fully consume their work. Any modification of their
      operands other than invoking another pipeline is disallowed.

      Important: To achieve bubble-free execution, it is important to also use
      the manual allocation mode by calling ``get_allocations`` on the returned
      function, passing the result to ``pl.run_scoped`` and the provided results
      to the returned function as an ``allocations`` keyword argument.
      Otherwise, the pipeline function will perform the scoped allocation itself
      which can lead to synchronization that can still cause pipeline bubbles.
  """

  # TODO(justinfu): Factor out common code between warp-specialized and
  # normal pipelines.
  if not isinstance(in_specs, (list, tuple)):
    in_specs = (in_specs,)
  if not isinstance(out_specs, (list, tuple)):
    out_specs = (out_specs,)
  if isinstance(in_specs, list):
    in_specs = tuple(in_specs)
  if isinstance(out_specs, list):
    out_specs = tuple(out_specs)

  flat_in_specs, in_specs_treedef = jax.tree.flatten(in_specs)
  flat_in_specs = tuple(map(_downcast_spec, flat_in_specs))
  for spec in flat_in_specs:
    if len(spec.collective_axes) > 1:
      raise ValueError(
          "Only a single collective axis supported in input BlockSpecs, but"
          f" got {spec.collective_axes}"
      )
  collective_axes = tuple(frozenset(
      a for spec in flat_in_specs for a in spec.collective_axes
  ))
  flat_out_specs, out_specs_treedef = jax.tree.flatten(out_specs)
  flat_out_specs = tuple(map(_downcast_spec, flat_out_specs))
  for spec in flat_out_specs:
    if spec.collective_axes:
      raise ValueError("Output BlockSpecs cannot have collective_axes")
  delay_release = -1
  for in_spec in in_specs:
    if not isinstance(in_spec, gpu_core.BlockSpec):
      delay_release = 0
      continue
    if delay_release >= 0 and in_spec.delay_release != delay_release:
      raise NotImplementedError(
          "All inputs must have the same delay_release, but"
          f" {in_spec.delay_release=} != {delay_release=}"
      )
    delay_release = in_spec.delay_release

  delay_release = max(delay_release, 0)
  if max_concurrent_steps <= delay_release:
    raise ValueError(
        "max_concurrent_steps must be greater than delay_release, but"
        f" {max_concurrent_steps=}, {delay_release=}"
    )

  if memory_thread_idx is None:
    memory_thread_idx = num_compute_wgs
  if memory_thread_idx != num_compute_wgs:
    # TODO(justinfu): Indexing calculations for buffers assume the memory
    # thread is the last thread.
    raise NotImplementedError("Memory thread must be the last thread.")

  has_carry = compute_context is not None

  # Trace the index maps to determine if they depend on the grid.
  # Grid-independent values will not be multiple-buffered.
  in_spec_has_seq_axis = [
      not _is_index_invariant(spec, grid) for spec in flat_in_specs]
  out_spec_has_seq_axis = [
      not _is_index_invariant(spec, grid) for spec in flat_out_specs]
  spec_has_seq_axis = [*in_spec_has_seq_axis, *out_spec_has_seq_axis]
  if not all(in_spec_has_seq_axis):
    raise NotImplementedError("Only inputs with a dependency on the grid are supported.")

  num_steps = math.prod(grid)
  has_dynamic_grid = not isinstance(num_steps, int)

  def _get_slot(step, has_seq_dim):
    """Returns the buffer slot given the pipeline step."""
    if has_seq_dim:
      return step
    else:
      return 0

  # Shrink ``max_concurrent_steps`` if the total number of steps is lower to
  # reduce the size of the refs allocated in SMEM.
  if not has_dynamic_grid and max_concurrent_steps > num_steps:
    max_concurrent_steps = int(num_steps)

  def _get_scoped_allocs(*gmem_refs: AbstractRefPytree):
    in_gmem_refs = gmem_refs[:len(in_specs)]
    out_gmem_refs = gmem_refs[len(in_specs):]
    flat_in_gmem_refs, in_gmem_refs_treedef = jax.tree.flatten(in_gmem_refs)
    flat_out_gmem_refs, out_gmem_refs_treedef = jax.tree.flatten(out_gmem_refs)
    if in_specs_treedef != in_gmem_refs_treedef:
      raise ValueError(
          "Input specs and input gmem refs must have the same pytree structure."
          f" {in_specs_treedef} != {in_gmem_refs_treedef}"
      )
    if out_specs_treedef != out_gmem_refs_treedef:
      raise ValueError(
          "Output specs and output gmem refs must have the same pytree structure."
          f" {out_specs_treedef} != {out_gmem_refs_treedef}"
      )
    flat_gmem_refs = [*flat_in_gmem_refs, *flat_out_gmem_refs]
    smem_allocs = []
    for spec, has_seq_dim, gmem_ref in zip(
        it.chain(flat_in_specs, flat_out_specs),
        spec_has_seq_axis,
        flat_gmem_refs):
      slots = max_concurrent_steps if has_seq_dim else 1
      smem_allocs.append(
          gpu_core.SMEM(
              (slots, *_get_block_shape(spec, gmem_ref.shape)),
              gmem_ref.dtype,
              transforms=getattr(spec, "transforms", ()),
          )
      )
    flat_in_smem_refs, flat_out_smem_refs = util.split_list(
        smem_allocs, [len(flat_in_specs)])
    in_smem_barrier = gpu_core.Barrier(
        num_arrivals=len(flat_in_specs), num_barriers=max_concurrent_steps
    )
    flat_consumed_barriers: list[gpu_core.Barrier | gpu_core.ClusterBarrier]
    flat_consumed_barriers = []
    consumed_barrier_type: Any
    if collective_axes:
      consumed_barrier_type = functools.partial(
          gpu_core.ClusterBarrier, collective_axes=collective_axes
      )
    else:
      consumed_barrier_type = gpu_core.Barrier
    for _ in flat_in_specs:
      if manual_consumed_barriers:
        flat_consumed_barriers.append(
            consumed_barrier_type(
                num_arrivals=num_compute_wgs,
                num_barriers=max_concurrent_steps,
            )
        )
    if not manual_consumed_barriers:
      # We only allocated one consumed barrier for all inputs when using
      # automatic consumed barriers.
      flat_consumed_barriers = [
          consumed_barrier_type(
              num_arrivals=num_compute_wgs,
              num_barriers=max_concurrent_steps,
          )
      ]
    return dict(
        flat_in_smem_refs=flat_in_smem_refs,
        flat_out_smem_refs=flat_out_smem_refs,
        in_smem_barrier_ref=in_smem_barrier,
        flat_consumed_barrier_refs=flat_consumed_barriers,
    )

  def pipeline(*gmem_refs: AbstractRefPytree, allocations: Any | None = None):
    """
    Run the pipeline.

    Args:
      *gmem_refs: A list of pytrees of pallas refs
      allocations: The allocation provided by ``pl.run_scoped`` when the result
        of calling ``get_allocations(*gmem_refs)`` is passed to
        ``pl.run_scoped``.
    """
    in_gmem_refs = gmem_refs[:len(in_specs)]
    out_gmem_refs = gmem_refs[len(in_specs):]
    flat_in_gmem_refs, in_gmem_refs_treedef = jax.tree.flatten(in_gmem_refs)
    flat_out_gmem_refs, out_gmem_refs_treedef = jax.tree.flatten(out_gmem_refs)
    if in_specs_treedef != in_gmem_refs_treedef:
      raise ValueError(
          "Input specs and input gmem refs must have the same pytree structure."
          f" {in_specs_treedef} != {in_gmem_refs_treedef}"
      )
    if out_specs_treedef != out_gmem_refs_treedef:
      raise ValueError(
          "Output specs and output gmem refs must have the same pytree structure."
          f" {out_specs_treedef} != {out_gmem_refs_treedef}"
      )

    if allocations is None:
      if pipeline_state is not None:
        raise ValueError(
            "Pipeline state should not be set when using automatic allocation."
        )
      return pl.run_scoped(
          functools.partial(
              scoped_pipeline,
              flat_in_gmem_refs=flat_in_gmem_refs,
              flat_out_gmem_refs=flat_out_gmem_refs,
          ),
          **_get_scoped_allocs(*gmem_refs),
          collective_axes=wg_axis,
      )
    else:
      scoped_pipeline(
          flat_in_gmem_refs=flat_in_gmem_refs,
          flat_out_gmem_refs=flat_out_gmem_refs,
          **allocations,
      )

  pipeline.get_allocations = _get_scoped_allocs  # pyrefly: ignore[missing-attribute]

  def scoped_pipeline(
      *,
      flat_in_gmem_refs,
      flat_out_gmem_refs,
      flat_in_smem_refs,
      flat_out_smem_refs,
      in_smem_barrier_ref,
      flat_consumed_barrier_refs,
  ):
    flat_in_brefs: Sequence[BufferedRef] = [
        BufferedRef(spec, not has_seq_axis, gmem_ref, smem_ref)
        for spec, has_seq_axis, gmem_ref, smem_ref in zip(
            flat_in_specs, in_spec_has_seq_axis, flat_in_gmem_refs, flat_in_smem_refs
        )
    ]
    flat_out_brefs: Sequence[BufferedRef] = [
        BufferedRef(spec, not has_seq_axis, gmem_ref, smem_ref)
        for spec, has_seq_axis, gmem_ref, smem_ref in zip(
            flat_out_specs, out_spec_has_seq_axis, flat_out_gmem_refs, flat_out_smem_refs
        )
    ]

    def compute_block():
      gpu_primitives.set_max_registers(
          _compute_registers(memory_registers, num_compute_wgs),
          action="increase")

      # This is true if any of the outputs need to be transferred inside the loop.
      smem_out_brefs = [bref for bref in flat_out_brefs if _in_smem(bref.spec)]
      # The implementation below has races when we have multiple compute WGs.
      # The problem is that we expect the compute WGs to deal with issuing the
      # SMEM->GMEM copies, but (1) we never predicate them, so we repeat the
      # same copy multiple times, and (2) we don't synchronize the compute WGs
      # in any way. In the unlikely event that one of the compute WGs runs 2
      # steps ahead, it might start overwriting the output buffer before the
      # other WG has issued its copy.
      #
      # The best fix here would be to move the SMEM->GMEM copies into the memory
      # WG and use proper barriers (with arrival_count=2) to ensure all WGs have
      # produced their outputs before it is sent out to GMEM.
      if smem_out_brefs and num_compute_wgs > 1:
        raise NotImplementedError(
            "SMEM outputs are not supported with multiple compute warpgroups"
        )
      copies_out_in_loop = not all(bref.is_index_invariant for bref in smem_out_brefs)
      needs_epilogue = any(bref.is_index_invariant for bref in smem_out_brefs)

      def compute_loop_body(step, carry):
        indices, last_store_indices, prev_body_carry = carry
        slot = lax.rem(step, max_concurrent_steps)
        consumed_slot = lax.rem(step - delay_release, max_concurrent_steps)
        # Wait for the current GMEM->SMEM copies to complete.
        gpu_primitives.barrier_wait(in_smem_barrier_ref.at[_get_slot(slot, True)])

        # Wait for the previous output SMEM->GMEM copy to complete.
        if copies_out_in_loop:
          gpu_primitives.wait_smem_to_gmem(
              max_concurrent_steps - 1, wait_read_only=True
          )

        in_brefs = jax.tree.unflatten(in_specs_treedef, flat_in_brefs)
        out_brefs = jax.tree.unflatten(out_specs_treedef, flat_out_brefs)
        all_brefs = (*in_brefs, *out_brefs)
        body_args = map_brefs(
            lambda bref: bref.get_ref_for_slot(
                _get_slot(slot, not bref.is_index_invariant)
            ),
            all_brefs,
        )

        if manual_consumed_barriers:
          barriers = jax.tree.unflatten(
              in_specs_treedef,
              [barrier.at[consumed_slot] for barrier in flat_consumed_barrier_refs],
          )
          body_args = (*body_args, *barriers)
        if has_carry:
          body_args = (*body_args, prev_body_carry)
        next_body_carry = body(indices, *body_args)

        if not manual_consumed_barriers:
          [consumed_barrier_ref] = flat_consumed_barrier_refs
          if delay_release > 0:
            lax.cond(
                step < delay_release,
                lambda: None,
                lambda: gpu_primitives.barrier_arrive(consumed_barrier_ref.at[consumed_slot]),
            )
          else:
            gpu_primitives.barrier_arrive(consumed_barrier_ref.at[consumed_slot])
        # TODO(justinfu,apaszke): This should probably be done by the memory WG.
        # Copy the output from SMEM to GMEM.
        if copies_out_in_loop:
          gpu_primitives.commit_smem()

        new_store_indices = last_store_indices[:]
        for idx, bref in enumerate(flat_out_brefs):
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
          bref.copy_out(_get_slot(slot, not bref.is_index_invariant),
                        indices,
                        predicate=slices_changed)
        gpu_primitives.commit_smem_to_gmem_group()
        next_indices = _inc_grid_by_1(indices, grid)
        return (next_indices, new_store_indices, next_body_carry)
      init_indices = (jnp.asarray(0, dtype=jnp.int32),) * len(grid)

      # TODO(justinfu): Only store base pointer instead of all indices.
      last_store_indices = [
          None
          if bref.is_index_invariant
          # pyrefly: ignore[bad-argument-type]
          else (jnp.array(-1),) * len(bref.spec.block_shape)
          for bref in flat_out_brefs
      ]

      if has_carry:
        last_indices = None
        def pipeline_callback(user_init_carry):
          nonlocal last_indices
          if last_indices is not None:
            raise ValueError(
              "Cannot call pipeline more than once in `compute_context`")
          init_loop_carry = (init_indices, last_store_indices, user_init_carry)
          last_indices, _, final_body_carry = lax.fori_loop(0,
                        num_steps,
                        compute_loop_body,
                        init_loop_carry)
          return final_body_carry
        assert compute_context is not None
        compute_context(pipeline_callback)
        if last_indices is None:
          raise ValueError("Pipeline was not called in `compute_context`")
      else:
        assert compute_context is None
        last_indices, _, _ = lax.fori_loop(
            0, num_steps, compute_loop_body,
            (init_indices, last_store_indices, None)
        )

      # Handle index_invariant outputs after the loop. They are not
      # written in the main pipeline loop.
      if not copies_out_in_loop and needs_epilogue:
        gpu_primitives.commit_smem()

      if needs_epilogue:
        last_slot = lax.rem(num_steps - 1, max_concurrent_steps)
        for bref in flat_out_brefs:
          if bref.is_index_invariant:
            bref.copy_out(_get_slot(last_slot, has_seq_dim=False),
                          last_indices, predicate=None)

        gpu_primitives.commit_smem_to_gmem_group()

      if smem_out_brefs:
        # Finalize the pipeline.
        gpu_primitives.wait_smem_to_gmem(0)

    # The memory thread executes this block which issues all pipelined DMAs.
    # TODO(apaszke,justinfu): Use a single arrive_expect_tx for all transfers.
    def memory_block():
      gpu_primitives.set_max_registers(memory_registers, action="decrease")
      indices = (jnp.asarray(0, dtype=jnp.int32),) * len(grid)
      if has_dynamic_grid:
        prologue_steps = lax.min(max_concurrent_steps, num_steps)
      else:
        assert max_concurrent_steps <= num_steps
        prologue_steps = max_concurrent_steps
      pipeline_init_prologue_steps = prologue_steps
      if pipeline_state is not None:
        if has_dynamic_grid:
          raise NotImplementedError(
              "A pipeline of pipelines is not supported with dynamic grids"
          )
        if num_steps % max_concurrent_steps:
          raise NotImplementedError(
              "A pipeline of pipelines is only allowed when the number of steps"
              f" (product of grid, here {num_steps}) is divisible by"
              f" {max_concurrent_steps=}"
          )
        if delay_release:
          raise NotImplementedError(
              "A pipeline of pipelines is not supported with delay_release"
          )
        if isinstance(pipeline_state, PipelinePipeline):
          prologue_steps = prologue_steps if pipeline_state == PipelinePipeline.START else 0
        else:
          prologue_steps = jnp.where(pipeline_state == PipelinePipeline.START, prologue_steps, 0)

      # Begin initial copies.
      def _init_step(step, indices):
        for bref in flat_in_brefs:
          buf_slot = _get_slot(step, not bref.is_index_invariant)
          barrier_slot = _get_slot(step, True)
          bref.copy_in(buf_slot, indices, in_smem_barrier_ref, barrier_slot)
        return _inc_grid_by_1(indices, grid)

      indices = jax.lax.fori_loop(
          0, prologue_steps, _init_step, indices, unroll=not has_dynamic_grid
      )

      def memory_loop_body(step, carry):
        indices, = carry
        slot = lax.rem(step, max_concurrent_steps)
        fetch_slot = slot  # (x + y) % y == x % y

        if not manual_consumed_barriers:
          # We only have one consumed barrier when using automatic consumed
          # barrier management.
          [consumed_barrier_ref] = flat_consumed_barrier_refs
          gpu_primitives.barrier_wait(consumed_barrier_ref.at[slot])
          consumed_barrier_it = [None] * len(flat_in_brefs)
        else:
          consumed_barrier_it = flat_consumed_barrier_refs

        for bref, consumed_barrier in zip(flat_in_brefs, consumed_barrier_it):
          if manual_consumed_barriers:
            assert consumed_barrier is not None
            gpu_primitives.barrier_wait(consumed_barrier.at[slot])
          buf_slot = _get_slot(fetch_slot, not bref.is_index_invariant)
          barrier_slot = _get_slot(fetch_slot, True)
          bref.copy_in(buf_slot, indices, in_smem_barrier_ref, barrier_slot)
        next_indices = _inc_grid_by_1(indices, grid)
        return (next_indices,)
      lax.fori_loop(0, num_steps - prologue_steps, memory_loop_body, (indices,))
      # Await all the arrivals to not leave barriers in a bad state.
      # We only need to account for the prologue steps, only the first
      # delay_release of them skip arrivals, so we subtract them.
      @pl.when(pipeline_state is None or pipeline_state == PipelinePipeline.STOP)
      def _quiesce():
        @pl.loop(
            num_steps - pipeline_init_prologue_steps,
            num_steps - delay_release,
            unroll=not has_dynamic_grid,
        )
        def _epi_step(step):
          consumed_slot = lax.rem(step, max_concurrent_steps)
          for barrier in flat_consumed_barrier_refs:
            gpu_primitives.barrier_wait(barrier.at[consumed_slot])

    wg_idx = lax.axis_index(wg_axis)
    lax.cond(
        wg_idx != memory_thread_idx,
        compute_block,
        memory_block
    )
  # Type checkers do not understand the get_allocations assignment above.
  return pipeline  # pyrefly: ignore[bad-return]

