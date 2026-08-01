
def lift_fwd(num_consts: int, fwd_jaxpr_thunk: lu.WrappedFun) -> lu.WrappedFun:
  def fwd(*args):
    vals, nonzeros = args[::2], args[1::2]
    assert len(vals) == len(nonzeros)
    _, primals = split_list(vals, [num_consts])
    const_nonzeros, in_nonzeros = split_list(nonzeros, [num_consts])
    if any(const_nonzeros): raise ad.CustomVJPException()
    fwd_jaxpr, fwd_consts = fwd_jaxpr_thunk.call_wrapped(*in_nonzeros)
    return core.eval_jaxpr(fwd_jaxpr, fwd_consts, *primals)
  return lu.wrap_init(fwd, debug_info=fwd_jaxpr_thunk.debug_info)

