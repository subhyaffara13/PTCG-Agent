
def _custom_vjp_call_physicalize_rule(
    ctx: Context, *args, call_jaxpr, num_consts, fwd_jaxpr_thunk, bwd, **kwargs
):
  _assert_no_fusion_types(ctx.avals_out)
  new_jaxpr = physicalize_closed_jaxpr(call_jaxpr)
  fun = lu.wrap_init(core.jaxpr_as_fun(new_jaxpr),
                     debug_info=call_jaxpr.jaxpr.debug_info)
  fwd = custom_derivatives.lift_fwd(num_consts, fwd_jaxpr_thunk)
  fwd_physicalized = _physicalize_transform(fwd)
  const_avals, _ = util.split_list(new_jaxpr.in_avals, [num_consts])
  bwd_physicalized = _physicalize_transform_bwd(bwd, const_avals)
  kwargs['subfuns'] = (fun, fwd_physicalized, bwd_physicalized)
  return custom_derivatives.custom_vjp_call_p.bind(*args, **kwargs)

