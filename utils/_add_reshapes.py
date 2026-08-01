
def _add_reshapes(which: Sequence[bool],
                  jaxpr_known: core.Jaxpr,
                  jaxpr_staged: core.Jaxpr) -> tuple[core.Jaxpr, core.Jaxpr]:
  # add singleton axes to residuals which are from jaxpr_known and are scalars
  which_ = [w and not v.aval.shape  # pyrefly: ignore[missing-attribute]
            for w, v in zip(which, jaxpr_staged.invars[:len(which)])]
  if not any(which_): return jaxpr_known, jaxpr_staged
  assert not jaxpr_known.constvars and not jaxpr_staged.constvars

  def known(*args):
    out = eval_jaxpr_p.bind(*args, jaxpr=core.ClosedJaxpr(jaxpr_known, ()))
    out_known, res = split_list(out, [len(out) - sum(which)])
    res = [_add_singleton(x) if not x.shape else x for x in res]
    return [*out_known, *res]
  avals_in = tuple(v.aval for v in jaxpr_known.invars)
  avals_in = FlatTree.flatten((avals_in, {}))
  jaxpr_known_closed, _ = pe.trace_to_jaxpr(
      known, avals_in, debug_info=jaxpr_known.debug_info)

  def staged(*args):
    res_, ins = split_list(args, [len(which)])
    res = [_rem_singleton(x) if w else x for x, w in zip(res_, which_)]
    closed_jaxpr_staged = core.ClosedJaxpr(jaxpr_staged, ())
    return eval_jaxpr_p.bind(*res, *ins, jaxpr=closed_jaxpr_staged)
  res_avals = [core.unmapped_aval(1, 0, v.aval) if w else v.aval
               for w, v in zip(which_, jaxpr_staged.invars[:len(which)])]
  avals_in = (*res_avals, *[v.aval for v in jaxpr_staged.invars[len(which):]])
  avals_in = FlatTree.flatten((avals_in, {}))
  jaxpr_staged_closed, _ = pe.trace_to_jaxpr(
      staged, avals_in, debug_info=jaxpr_staged.debug_info)

  return jaxpr_known_closed.jaxpr, jaxpr_staged_closed.jaxpr

