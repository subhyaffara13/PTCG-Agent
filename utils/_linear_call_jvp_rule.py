
def _linear_call_jvp_rule(primals, tangents, callee, transpose_thunk,
                          num_callee_consts, num_res):
  consts_and_res, primals = split_list(primals, [num_callee_consts + num_res])
  const_tangents, tangents = split_list(tangents, [num_callee_consts + num_res])
  assert all(type(t) is Zero for t in const_tangents)
  primals_out = linear_call_p.bind(
      *consts_and_res, *primals, callee=callee, transpose_thunk=transpose_thunk,
      num_callee_consts=num_callee_consts, num_res=num_res)
  tangents_out = linear_call_p.bind(
      *consts_and_res, *tangents, callee=callee, transpose_thunk=transpose_thunk,
      num_callee_consts=num_callee_consts, num_res=num_res)
  return primals_out, tangents_out

