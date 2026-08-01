
def _custom_vjp_call_dce(
    used_outs: Sequence[bool], eqn: core.JaxprEqn
) -> tuple[list[bool], core.JaxprEqn | None]:
  if not any(used_outs) and not pe.has_effects(eqn):
    return [False] * len(eqn.invars), None
  call_jaxpr: core.ClosedJaxpr = eqn.params["call_jaxpr"]
  fwd_jaxpr_thunk = eqn.params["fwd_jaxpr_thunk"]
  bwd: lu.WrappedFun = eqn.params["bwd"]
  out_trees: Callable[[], tuple[PyTreeDef, PyTreeDef, list[int | None]]] = eqn.params["out_trees"]
  symbolic_zeros: bool = eqn.params["symbolic_zeros"]
  dce_call_jaxpr: core.ClosedJaxpr
  used_ins: Sequence[bool]
  dce_call_jaxpr, used_ins = _cached_closed_call_dce_instantiate(
      call_jaxpr, tuple(used_outs))
  assert all(used_ins)

  @partial(lu.wrap_init, debug_info=fwd_jaxpr_thunk.debug_info)
  @pe._memoize
  def dce_fwd_jaxpr_thunk(*zeros):
    fwd_jaxpr = core.ClosedJaxpr(*fwd_jaxpr_thunk.call_wrapped(*zeros))
    _, res_tree, fwds = out_trees()
    num_res_out = res_tree.num_leaves - sum(f is not None for f in fwds)
    dce_fwd_jaxpr, _ = _cached_closed_call_dce_instantiate(
        fwd_jaxpr, (True,) * num_res_out + tuple(used_outs))
    return dce_fwd_jaxpr.jaxpr, dce_fwd_jaxpr.consts

  def dce_bwd(*args):
    _, res_tree, _ = out_trees()
    res, cts = split_list(args, [res_tree.num_leaves])
    cts_ = iter(cts)
    all_cts = []
    for used, aval in zip(used_outs, call_jaxpr.out_avals):
      if used:
        all_cts.append(next(cts_))
      else:
        ct_aval = aval.to_ct_aval()
        if symbolic_zeros:
          all_cts.append(SymbolicZero(ct_aval))
        else:
          all_cts.append(zeros_like_aval(ct_aval))
    assert next(cts_, None) is None
    return bwd.call_wrapped(*res, *all_cts)

  dce_bwd_wrapped = lu.wrap_init(dce_bwd,
                                 debug_info=bwd.debug_info)
  outvars = [v for used, v in zip(used_outs, eqn.outvars) if used]
  new_params = dict(
      eqn.params,
      call_jaxpr=dce_call_jaxpr,
      fwd_jaxpr_thunk=dce_fwd_jaxpr_thunk,
      bwd=dce_bwd_wrapped,
  )
  new_eqn = pe.new_jaxpr_eqn(
      eqn.invars, outvars, eqn.primitive, new_params,
      core.eqn_effects(dce_call_jaxpr, eqn.invars),
      eqn.source_info, eqn.ctx)
  return list(used_ins), new_eqn

