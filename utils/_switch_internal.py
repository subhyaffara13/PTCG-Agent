from typing import Any, Callable

def _switch_internal(
    index: ArrayLike,
    branches: Sequence[Callable],
    operands: Sequence[Any], *,
    branches_platforms: BranchesPlatforms | None):
  if config.disable_jit.value and core.is_concrete(index):
    return branches[int(index)](*operands)  # pyrefly: ignore[bad-argument-type]

  dbgs = [api_util.debug_info("switch", branch, operands, {})
          for branch in branches]
  args = FlatTree.flatten((operands, {}))
  avals = args.map(core.typeof)

  if config.mutable_array_checks.value:
    api_util.check_no_aliased_ref_args(lambda: dbgs[0], list(avals), list(args))

  jaxprs_, out_avalss = zip(*[pe.trace_to_jaxpr(branch, avals, dbg)
                             for branch, dbg in zip(branches, dbgs)])
  jaxprs_, all_consts = zip(*[pe.separate_consts(j) for j in jaxprs_])
  jaxprs, consts = _merge_common_consts(jaxprs_, all_consts)

  if config.mutable_array_checks.value:
    api_util._check_no_aliased_closed_over_refs(dbgs[0], (*jaxprs[0].consts, *consts), list(args))
  for i, (out_avals, jaxpr) in enumerate(zip(out_avalss[1:], jaxprs[1:])):
    _check_branch_outputs(
        "switch", "branch 0", f"branch{i+1}", branches[0], branches[i+1],
        out_avalss[0], out_avals)
  # prune passthrough outputs
  fwds = [pe._jaxpr_forwarding(jaxpr.jaxpr) for jaxpr in jaxprs]
  in_fwd = [xs[0] if len(set(xs)) == 1 else None for xs in zip(*fwds)]
  keep = [f is None for f in in_fwd]
  jaxprs = [pe.prune_closed_jaxpr_outputs(jaxpr, keep) for jaxpr in jaxprs]

  joined_effects = core.join_effects(
      *(core.positional_effects(jaxpr) for jaxpr in jaxprs))
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `switch`: {disallowed_effects}')
  jaxprs = [replace_jaxpr_effects(
      jaxpr, core.resolve_input_effects(joined_effects, jaxpr.jaxpr.invars))
      for jaxpr in jaxprs]
  params = dict(branches=tuple(jaxprs))
  if branches_platforms is not None:
    params["branches_platforms"] = branches_platforms
  out = cond_p.bind(index, *consts, *args, **params)
  out_ = iter(out)

  all_inputs: list[Any] = [*consts, *args]
  out = [
    next(out_) if fwd is None else lax.asarray(all_inputs[fwd])
    for fwd in in_fwd
  ]
  assert next(out_, None) is None
  return out_avalss[0].update(out).unflatten()

