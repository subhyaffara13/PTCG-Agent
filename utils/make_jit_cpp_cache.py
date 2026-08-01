
def make_jit_cpp_cache(capacity):
  return _jax.PjitFunctionCache(capacity=capacity)

