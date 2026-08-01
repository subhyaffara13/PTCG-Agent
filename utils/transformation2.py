
def transformation2(gen, fun: WrappedFun, *gen_static_args) -> WrappedFun:
  """Adds one more transformation to a WrappedFun.

  Args:
    gen: the transformation generator function
    fun: a WrappedFun on which to apply the transformation
    gen_static_args: static args for the generator function
  """
  return fun.wrap(gen, gen_static_args, None)

