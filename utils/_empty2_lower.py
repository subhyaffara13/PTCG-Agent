
def _empty2_lower(ctx, *, dtype, memory_space):
  dtype = dtype if dtypes.issubdtype(dtype, dtypes.extended) else np.dtype(dtype)
  phys_aval = core.physical_aval(core.ShapedArray((), dtype))
  return [mlir.ir_constant(np.zeros(phys_aval.shape, phys_aval.dtype))]

