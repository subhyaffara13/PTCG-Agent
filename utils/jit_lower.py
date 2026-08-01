
def jit_lower(jit_func, *args, **kwargs):
  return jit_trace(jit_func, *args, **kwargs).lower()

