
def _linear_call_impl(*args, callee, transpose_thunk, num_callee_consts,
                      num_res):
  del transpose_thunk, num_callee_consts, num_res
  return core.eval_jaxpr(callee.jaxpr, (), *args)

