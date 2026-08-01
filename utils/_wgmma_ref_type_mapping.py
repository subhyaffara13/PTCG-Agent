
def _wgmma_ref_type_mapping(ref: WGMMAAccumulatorRef):
  aval = WGMMAAbstractAccumulatorRef(
      jax_core.ShapedArray(shape=ref.shape, dtype=ref.dtype), MemorySpace.REGS
  )
  return aval, ref._init

