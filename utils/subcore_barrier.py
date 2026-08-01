
def subcore_barrier():
  """Blocks until all subcores on the same core reach this instruction.

  The barrier must be used with
  :class:jax.experimental.pallas.tpu_sc.VectorSubcoreMesh.
  """
  barrier_p.bind()

