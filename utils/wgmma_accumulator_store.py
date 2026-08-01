
def wgmma_accumulator_store(acc_ref, val):
  if not isinstance(acc_ref.aval, gpu_core.WGMMAAbstractAccumulatorRef):
    raise TypeError(f"acc must be a WGMMAAccumulatorAbstractRef, got {acc_ref.aval=}")
  wgmma_accumulator_store_p.bind(acc_ref, val)

