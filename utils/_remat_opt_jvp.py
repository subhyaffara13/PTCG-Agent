
def _remat_opt_jvp(
    primals,
    tangents,
    *,
    num_consts: int,
    num_res: int,
    fwd_jaxpr: core.ClosedJaxpr,
    fun_jaxpr_thunk: Callable[[], tuple[core.Jaxpr, Sequence[Any]]],
):
  consts, primals = split_list(primals, [num_consts])
  consts_dot, tangents = split_list(tangents, [num_consts])
  # Tangents must be instantated in case we end up DCEing later.
  tangents = map(ad.instantiate_zeros, tangents)
  consts_nz = [not isinstance(t, Zero) for t in consts_dot]
  consts_dot = [c for nz, c in zip(consts_nz, consts_dot) if nz]
  in_nz = consts_nz + [True] * len(tangents)
  fwd_jaxpr_jvp_, out_nz = ad.jvp_jaxpr(fwd_jaxpr, in_nz, True)
  num_out = len(out_nz) - num_res
  fwd_jaxpr_jvp_ = ad.rearrange_binders(
      fwd_jaxpr_jvp_, [num_consts, len(primals)],
      [len(consts_dot), len(tangents)], [num_res, num_out], [num_res, num_out])
  fwd_jaxpr_jvp = pe.close_jaxpr(pe.convert_constvars_jaxpr(fwd_jaxpr_jvp_.jaxpr))

  # @pe._memoize
  def fun_jvp_jaxpr_thunk():
    fun_jaxpr = core.ClosedJaxpr(*fun_jaxpr_thunk())
    in_nz = [True] * len(primals)
    fun_jvp_jaxpr, _ = ad.jvp_jaxpr(fun_jaxpr, in_nz, True)
    return fun_jvp_jaxpr.jaxpr, fun_jvp_jaxpr.consts

  new_num_consts = len(fwd_jaxpr_jvp_.consts) + num_consts + len(consts_dot)
  outs = remat_opt_p.bind(*fwd_jaxpr_jvp_.consts, *consts, *consts_dot,
                          *primals, *tangents, num_consts=new_num_consts,
                          num_res=2 * num_res, fwd_jaxpr=fwd_jaxpr_jvp,
                          fun_jaxpr_thunk=fun_jvp_jaxpr_thunk)
  res, res_dot, outs, outs_dot = split_list(outs, [num_res, num_res, num_out])
  return (*res, *outs), (*res_dot, *outs_dot)

