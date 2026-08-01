
def _dimension_size_impl(arg, *, dimension):
  return core.dim_constant(arg.shape[dimension])

