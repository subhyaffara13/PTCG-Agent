
def _linear_call_transpose_rule(cts, *args, callee, transpose_thunk,
                                num_callee_consts, num_res):
  transpose, t_consts = transpose_thunk()
  f_consts, operands_res, operands_lin = split_list(
      args, [num_callee_consts, num_res])
  _, _, cts_avals = split_list(
      transpose.in_avals, [len(t_consts), num_res])

  assert all(ad.is_undefined_primal(x)     for x in operands_lin)
  assert all(not ad.is_undefined_primal(x) for x in operands_res)

  def new_transpose_thunk():
    return callee, f_consts

  cts = [zeros_like_aval(a) if type(ct) is Zero else ct
         for ct, a in zip(cts, cts_avals)]
  cts_out = linear_call_p.bind(*t_consts, *operands_res, *cts,
                               callee=transpose,
                               transpose_thunk=new_transpose_thunk,
                               num_callee_consts=len(t_consts),
                               num_res=len(operands_res))

  return [None] * (num_callee_consts + num_res) + cts_out

