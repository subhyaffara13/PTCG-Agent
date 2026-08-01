
def dynamic_scheduling_loop(
    grid_names: Sequence[Hashable],
    *,
    thread_axis: Hashable | None = None,
    cluster_axes: tuple[str | tuple[str, ...], ...] = (),
    init_carry: None = None
) -> Callable[[Callable[[NDLoopInfo], None]], None]:
  ...


def dynamic_scheduling_loop(
    grid_names: Sequence[Hashable],
    *,
    thread_axis: Hashable | None = None,
    cluster_axes: tuple[str | tuple[str, ...], ...] = (),
    init_carry: _T
) -> Callable[[Callable[[NDLoopInfo, _T], _T]], _T]:
  ...


def dynamic_scheduling_loop(
    grid_names,
    thread_axis = None,
    cluster_axes = (),
    init_carry = None):
  """A loop over program instances using dynamic work scheduling.

  This loop will iterate through available program instances until all
  work has been scheduled. The kernel should be instantiated with a grid
  equal to the logical amount of work to be done (as opposed to a persistent
  kernel where the grid is set to the number of cores). Each core running
  this loop will continuously query the next available block of work and
  the loop will terminate when the entire grid has been scheduled.

  Example usage::

    @plgpu.dynamic_scheduling_loop(grid_names)
    def body(loop_info):
      work(loop_info.index)  # do work...

  Args:
    grid_names: The names of the axes in the grid.
    thread_axis: The name of the thread axis. This must be passed in if
      the kernel uses multiple threads.
    cluster_axes: The name of **all** cluster axes. This must be passed in if
      the kernel uses a cluster size > 1.
    init_carry: An optional initial carry for the loop. If passed in, the
      body function should expect a ``carry`` keyword argument and return
      the next carry value.
  """
  num_slots = 2
  num_threads = 1 if thread_axis is None else lax.axis_size(thread_axis)
  user_carry = init_carry

  def decorator(body):
    def _scoped(try_cancel_buffer, try_cancel_barrier, cancel_used_barrier):
      def try_cancel_cond(carry):
        _, success, _, _ = carry
        return success

      def try_cancel_body(carry):
        grid_idx, _, wave_step, user_carry = carry
        loop_info = NDLoopInfo(
            index=grid_idx, local_index=wave_step, num_local_steps=None
        )
        slot = lax.rem(wave_step, jnp.int32(num_slots))

        @pallas_helpers.when(wave_step >= num_slots)
        def wait_until_slot_available():
          gpu_primitives.barrier_wait(cancel_used_barrier.at[slot])
          inline_ptx(_FENCE_PROXY_ASYNC_GENERIC_ACQUIRE_SHARED_CLUSTER)

        gpu_primitives.try_cluster_cancel(
            try_cancel_buffer.at[slot], try_cancel_barrier.at[slot]
        )

        if user_carry is None:
          body(loop_info)
        else:
          user_carry = body(loop_info, carry=user_carry)

        gpu_primitives.barrier_wait(try_cancel_barrier.at[slot])
        grid_idx, success = gpu_primitives.query_cluster_cancel(
            try_cancel_buffer.at[slot], grid_names=grid_names
        )
        inline_ptx(_FENCE_PROXY_ASYNC_GENERIC_RELEASE_SHARED_CTA)
        gpu_primitives.barrier_arrive(cancel_used_barrier.at[slot])
        return (grid_idx, success, wave_step + jnp.int32(1), user_carry)

      grid_idx = tuple(map(lax.axis_index, grid_names))
      init_carry = (grid_idx, True, jnp.int32(0), user_carry)
      final_carry = lax.while_loop(try_cancel_cond, try_cancel_body, init_carry)
      _, _, num_steps, final_user_carry = final_carry
      num_barriers_to_reset = lax.min(num_steps, jnp.int32(num_slots))

      @pallas_helpers.loop(jnp.int32(0), num_barriers_to_reset)
      def reset_cancel_barrier(slot):
        gpu_primitives.barrier_wait(cancel_used_barrier.at[slot])

      return None if user_carry is None else final_user_carry

    if cluster_axes:
      cancel_used_barrier = gpu_core.ClusterBarrier(
          collective_axes=cluster_axes,
          num_arrivals=num_threads,
          num_barriers=num_slots,
      )
    else:
      cancel_used_barrier = gpu_core.Barrier(
          num_arrivals=num_threads,
          num_barriers=num_slots,
      )
    try_cancel_barrier = gpu_core.Barrier(
        num_arrivals=num_threads,
        num_barriers=num_slots,
    )
    return pallas_primitives.run_scoped(
        _scoped,
        try_cancel_buffer=gpu_core.TryClusterCancelResult(num_slots),
        try_cancel_barrier=try_cancel_barrier,
        cancel_used_barrier=cancel_used_barrier,
        collective_axes=thread_axis,
    )
  return decorator

