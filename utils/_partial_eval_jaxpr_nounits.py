
def _partial_eval_jaxpr_nounits(
    jaxpr: ClosedJaxpr, in_unknowns: Sequence[bool],
    instantiate: bool | Sequence[bool], fwd: bool | Sequence[bool]):
  f = lu.wrap_init(core.jaxpr_as_fun(jaxpr), debug_info=jaxpr.jaxpr.debug_info)

  cell = []
  def fun(*known_vals_in):
    known_vals_in_ = iter(known_vals_in)
    unknown_avals = (a for a, uk in zip(jaxpr.in_avals, in_unknowns) if uk)
    in_pvals = [PartialVal.unknown(next(unknown_avals)) if uk
                else PartialVal.known(next(known_vals_in_)) for uk in in_unknowns]
    assert next(known_vals_in_, None) is next(unknown_avals, None) is None
    jaxpr_unknown_, (fwds, out_pvals, residuals, ()) = trace_to_subjaxpr_nounits_fwd(
        f, TraceTag(), jaxpr.jaxpr.debug_info, instantiate).call_wrapped(in_pvals)
    jaxpr_unknown = convert_constvars_jaxpr(jaxpr_unknown_)
    out_unknowns = [not pval.is_known() for pval in out_pvals]
    if type(fwd) is bool and not fwd:
      residuals_ = iter(residuals)
      residuals = [next(residuals_) if f is None else known_vals_in[f]
                   for f in fwds]
      assert next(residuals_, None) is None
      fwds = [None] * len(fwds)
    else:
      if type(fwd) is tuple:
        fwd_ = [f for f, uk in zip(fwd, in_unknowns) if not uk]
        residuals_, residuals = iter(residuals), []
        fwds = [residuals.append(next(residuals_)) if f is None else
                residuals.append(known_vals_in[f]) if not fwd_[f] else
                f for f in fwds]
      fwds, residuals = _include_consts_in_fwds(jaxpr.consts, fwds, residuals)
    res_avals = [core.typeof(r) for r in residuals]
    cell.append((out_unknowns, jaxpr_unknown, res_avals, fwds))
    known_vals_out = [pval.get_known() for pval in out_pvals if pval.is_known()]
    return [*known_vals_out, *residuals]

  known_avals = [a for a, uk in zip(jaxpr.in_aval_qdds, in_unknowns) if not uk]
  jaxpr_known, _, consts_known = trace_to_jaxpr_dynamic(
      lu.wrap_init(fun, debug_info=f.debug_info.with_unknown_names()),
      known_avals)
  (out_unknowns, jaxpr_unknown, res_avals, fwds), = cell

  if config.enable_checks.value:
    core.check_jaxpr(jaxpr_known)
    core.check_jaxpr(jaxpr_unknown)

  closed_jaxpr_known = ClosedJaxpr(jaxpr_known, consts_known)
  closed_jaxpr_unknown = ClosedJaxpr(jaxpr_unknown, ())
  return closed_jaxpr_known, closed_jaxpr_unknown, out_unknowns, res_avals, fwds

