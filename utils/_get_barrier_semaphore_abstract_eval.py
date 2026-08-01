
def _get_barrier_semaphore_abstract_eval():
  return state.AbstractRef(
      jax_core.ShapedArray((), pl_core.BarrierSemaphore()),
      tpu_core.MemorySpace.SEMAPHORE,
  )

