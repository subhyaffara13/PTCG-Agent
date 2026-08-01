
def jit_eval_shape(jit_func, *args, **kwargs):
  return jit_trace(jit_func, *args, **kwargs).out_info

