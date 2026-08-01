
def core_barrier(sem, *, core_axis_name: str):
  """Synchronizes all cores in a given axis."""
  num_cores = jax.lax.axis_size(core_axis_name)
  core_id = jax.lax.axis_index(core_axis_name)

  @pl_helpers.when(num_cores > 1)
  def _():
    with jax.named_scope("sync_cores"):

      def signal_core(i):
        # Don't signal ourself
        @pl_helpers.when(core_id != i)
        def _():
          pl_primitives.semaphore_signal(sem, 1, core_index=i)

      for i in range(num_cores):
        signal_core(i)
      pl_primitives.semaphore_wait(sem, num_cores - 1)

