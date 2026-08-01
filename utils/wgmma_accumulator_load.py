
def wgmma_accumulator_load(acc, *, wait_n: int | None = 0):
  """Dereferences an accumulator register.

  Before dereferencing, this operation waits until there is no more than
  ``wait_n`` WGMMA operations in flight. If ``wait_n`` is None, no
  synchronization is performed.
  """
  if wait_n is not None and wait_n < 0:
    raise ValueError(f"wait_n must be non-negative, got {wait_n=}")

  if not isinstance(acc.aval, gpu_core.WGMMAAbstractAccumulatorRef):
    raise TypeError(f"acc must be a WGMMAAccumulatorAbstractRef, got {acc.aval=}")

  return wgmma_accumulator_deref_p.bind(acc, wait_n=wait_n)

