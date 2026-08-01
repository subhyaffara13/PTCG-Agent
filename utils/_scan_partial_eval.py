
def _scan_partial_eval(trace, *tracers, reverse: bool,
                       length: int, num_consts: int, num_carry: int,
                       jaxpr: ClosedJaxpr, unroll: int):
  num_ys = len(jaxpr.out_avals) - num_carry
  unknowns = [not t.pval.is_known() for t in tracers]
  const_uk, init_uk, xs_uk = split_list(unknowns, [num_consts, num_carry])

  # Fixpoint computation of which carry elements are unknown. Each iteration
  # promotes at least one carry to unknown. We need at most len(carry)
  # iterations to decide carry_uk, plus one to prepare the jaxpr.
  carry_uk = init_uk
  # Don't allow forwarding from the carry or numpy.ndarrays.
  fwd = [
      (i < num_consts or i >= num_consts + num_carry) and
      not isinstance(t.pval.get_known(), np.ndarray)
      for i, t in enumerate(tracers)
  ]
  for _ in range(1 + len(carry_uk)):
    unknowns = const_uk + carry_uk + xs_uk
    jaxpr_known, jaxpr_unknown, out_uk, res_avals, in_fwd_res = \
        pe.partial_eval_jaxpr_nounits_fwd(
            jaxpr, unknowns, instantiate=carry_uk + [False] * num_ys, fwd=fwd)
    carry_uk_out, ys_uk = split_list(out_uk, [num_carry])
    if carry_uk_out == carry_uk:
      break
    else:
      carry_uk = _map(operator.or_, carry_uk, carry_uk_out)
  else:
    assert False, "Fixpoint not reached"
  num_res_out, num_res_in = len(res_avals), len(in_fwd_res)
  num_knowns_out = len(jaxpr_known.out_avals) - num_res_out
  num_consts_known = num_consts - sum(const_uk)
  num_carry_known = num_carry - sum(carry_uk)
  del res_avals, carry_uk_out

  # Instantiate those inputs which must be treated as unknown from the fixpoint.
  tracers = [trace.instantiate_const(t) if uk else t
             for t, uk in zip(tracers, unknowns)]
  known_ins   = [t.pval.get_known() for t in tracers if     t.pval.is_known()]

  # At this point all non-forwarded residuals are treated as extensive outputs
  # of jaxpr_known. Hoist out those that only depend on consts.
  #   Before: jaxpr_known: [*known_ins] -> [*known_outs, *non_fwd_res]
  #   After: jaxpr_known: [*known_consts_, *known_ins] -> [*known_outs, *ext_res]
  # where, modulo hoisted res not being broadcast, we have
  #   non_fwd_res = merge_lists(which_hoisted, ext_res, hoisted_res)
  known_consts, known_ins = split_list(known_ins, [num_consts_known])
  jaxpr_known, known_consts_, which_hoisted, hoisted_res = \
      _scan_known_hoisting(jaxpr_known, known_consts, num_res_out)
  del num_res_out  # changed

  # To make jaxpr_unknown match the scan calling convention, move to the back
  # binders that don't correspond to hoisted or const-forwarded residuals.
  #   Before: jaxpr_unknown: [*res, *unknown_ins] -> [*unkown_outs]
  #   After: jaxpr_unkonwn: [*int_res, *unknown_ins, *ext_res] -> [*unknown_outs]
  num_unk_in = len(jaxpr_unknown.in_avals) - num_res_in
  which_hoisted_ = iter(which_hoisted)
  res_to_move = [not next(which_hoisted_) if f is None else
                 f >= len(jaxpr.consts) + num_consts_known + num_carry_known
                 for f in in_fwd_res]
  assert next(which_hoisted_, None) is None
  jaxpr_unknown = pe.move_binders_to_back(
      jaxpr_unknown, res_to_move + [False] * num_unk_in)

  # Run the known part of the scan (if it has any outputs or effects).
  if not jaxpr_known.out_avals and not jaxpr_known.effects:
    known_outs_ext_res = []
  else:
    assert len(known_consts_) + len(known_ins) == len(jaxpr_known.in_avals)
    known_outs_ext_res = scan_p.bind(
        *known_consts_, *known_ins, jaxpr=jaxpr_known, reverse=reverse,
        length=length, num_consts=len(known_consts_),
        num_carry=num_carry_known, unroll=unroll)
  known_outs, ext_res = split_list(known_outs_ext_res, [num_knowns_out])

  # Complete non_fwd_res and then res, then split to match binders.
  non_fwd_res = merge_lists(which_hoisted, ext_res, hoisted_res)
  non_fwd_res_ = iter(non_fwd_res)
  res = [next(non_fwd_res_) if f is None
         else [*jaxpr.consts, *known_consts, *known_ins][f] for f in in_fwd_res]
  assert next(non_fwd_res_, None) is None
  int_res, ext_res = partition_list(res_to_move, res)

  # Create input tracers for jaxpr_unknown bind.
  unknown_inputs = [t for t in tracers if not t.pval.is_known()]
  int_res = _map(trace.new_instantiated_const, int_res)
  ext_res = _map(trace.new_instantiated_const, ext_res)
  # Create output tracers for jaxpr_unknown bind, adapting extensive shapes.
  carry_avals, y_avals = split_list(jaxpr_unknown.out_avals, [sum(carry_uk)])
  ys_avals = [core.unmapped_leading_aval(length, y_aval) for y_aval in y_avals]
  out_tracers = [pe.JaxprTracer(trace, pe.PartialVal.unknown(a), None)
                 for a in it.chain(carry_avals, ys_avals)]
  del carry_avals, y_avals
  # Create equation.
  name_stack = source_info_util.current_name_stack()[len(trace.name_stack):]
  source = source_info_util.current().replace(name_stack=name_stack)
  unknown_tracers_in = [*int_res, *unknown_inputs, *ext_res]
  eqn = pe.new_eqn_recipe(trace, unknown_tracers_in, out_tracers, scan_p,
                          dict(reverse=reverse, length=length, unroll=unroll,
                               jaxpr=jaxpr_unknown,
                               num_consts=len(int_res) + sum(const_uk),
                               num_carry=sum(carry_uk)),
                          core.positional_effects(jaxpr_unknown), source)
  for t in out_tracers: t.recipe = eqn
  if effects.partial_eval_kept_effects.filter_in(jaxpr_unknown.effects):
    trace.effect_handles.append(pe.EffectHandle(unknown_tracers_in, eqn))

  # Merge known and unknown outputs into final result.
  return util.merge_lists(out_uk, known_outs, out_tracers)

