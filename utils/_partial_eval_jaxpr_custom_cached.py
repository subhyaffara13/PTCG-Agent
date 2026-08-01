
def _partial_eval_jaxpr_custom_cached(
    jaxpr: Jaxpr,
    in_unknowns: tuple[bool, ...],
    in_inst: tuple[bool, ...],
    ensure_out_unknowns: tuple[bool, ...],
    ensure_out_inst: tuple[bool, ...],
    saveable: Callable[..., RematCases_],
  ) -> tuple[Jaxpr, Jaxpr, list[bool], list[bool], int, int]:
  env: dict[Var, tuple[bool, bool]] = {}
  residuals: OrderedSet[Var] = OrderedSet()
  residual_refs: OrderedSet[Var] = OrderedSet()

  def read(x: Atom) -> tuple[bool, bool]:
    if type(x) is Var:
      return env[x]
    return (False, True)

  def write(unk: bool, inst: bool, v: Var) -> None:
    assert (unk, inst) != (True, False)
    env[v] = (unk, inst)

  def ensure_instantiated(inst: bool, x: Atom) -> Atom:
    if type(x) is Var and not inst:
      residuals.add(x)
    return x

  def has_effects(effects) -> bool:
    not_really_effects = (core.NamedAxisEffect, core.InternalMutableArrayEffect)
    return any(not isinstance(e, not_really_effects) for e in effects)

  known_eqns, staged_eqns = [], []
  foreach(write, in_unknowns, in_inst, jaxpr.invars)
  foreach(partial(write, False, True), jaxpr.constvars)
  for eqn in jaxpr.eqns:
    unks_in, inst_in = unzip2(map(read, eqn.invars))
    rule = partial_eval_jaxpr_custom_rules.get(eqn.primitive)
    if rule:
      eqn1, eqn2, unks_out, inst_out, res = rule(saveable, unks_in, inst_in, eqn)
      eqn1 and known_eqns.append(eqn1); eqn2 and staged_eqns.append(eqn2)
      for r in res:
        if isinstance(r.aval, AbstractRef):
          residual_refs.add(r)
        else:
          residuals.add(r)
      foreach(write, unks_out, inst_out, eqn.outvars)
    elif any(unks_in):
      inputs = map(ensure_instantiated, inst_in, eqn.invars)
      staged_eqns.append(eqn.replace(invars=inputs))
      foreach(partial(write, True, True), eqn.outvars)
    else:
      known_eqns.append(eqn)
      # If it's an effectful primitive, we always to run and avoid staging it.
      policy = ensure_enum(saveable(
          eqn.primitive, *[x.aval for x in eqn.invars], **eqn.params))
      if has_effects(eqn.effects) or isinstance(policy, SaveableType):
        foreach(partial(write, False, False), eqn.outvars)
      elif isinstance(policy, Offloadable):
        # TODO(slebedev): This is a legit error which requires a BUILD fix.
        from jax._src.dispatch import device_put_p, ArrayCopySemantics  # pyrefly: ignore[missing-import]
        resvars = [Var(v.aval.update(memory_space=core.mem_kind_to_space(policy.dst)))
                   for v in eqn.outvars]
        offload_eqn = core.JaxprEqn(
            eqn.outvars, resvars, device_put_p,
            dict(
                devices=(core.mem_kind_to_space(policy.dst),) * len(eqn.outvars),
                srcs=(None,),
                copy_semantics=(ArrayCopySemantics.ALWAYS_COPY,),
            ),
            set(), source_info_util.new_source_info(), core.current_jaxpr_eqn_context())
        known_eqns.append(offload_eqn)
        # resvars are known and available in the backward jaxpr.
        foreach(partial(write, False, True), resvars)
        assert all(o.aval.memory_space == core.mem_kind_to_space(policy.src)  # pyrefly: ignore[missing-attribute]
                   for o in eqn.outvars)
        residuals.update(resvars)
        reload_eqn = core.JaxprEqn(
            resvars, eqn.outvars, device_put_p,
            dict(
              devices=(core.mem_kind_to_space(policy.src),) * len(resvars),
              srcs=(None,),
              copy_semantics=(ArrayCopySemantics.ALWAYS_COPY,)
            ),
            set(), source_info_util.new_source_info(), core.current_jaxpr_eqn_context())
        staged_eqns.append(reload_eqn)
        # outvars are known and available in the backward jaxpr.
        foreach(partial(write, False, True), eqn.outvars)
      else:
        assert isinstance(policy, RecomputeType)
        inputs = map(ensure_instantiated, inst_in, eqn.invars)
        staged_eqns.append(eqn.replace(invars=inputs))
        foreach(partial(write, False, True), eqn.outvars)
  unzipped = unzip2(map(read, jaxpr.outvars))
  out_unknowns, out_inst = list(unzipped[0]), list(unzipped[1])
  assert all(type(v) is Var for v in residuals), residuals

  for x, inst, ensure_inst in zip(jaxpr.outvars, out_inst, ensure_out_inst):
    if ensure_inst: ensure_instantiated(inst, x)
  out_unknowns = map(op.or_, out_unknowns, ensure_out_unknowns)
  out_inst     = map(op.or_, out_inst,     ensure_out_inst)

  ins_known, _ = partition_list(in_unknowns, jaxpr.invars)
  outs_known, _ = partition_list(out_unknowns, jaxpr.outvars)
  ref_res_is_input = [r in ins_known for r in residual_refs]
  non_input_res_refs, _ = partition_list(ref_res_is_input, list(residual_refs))
  ins_known_and_ref_res = [*ins_known, *non_input_res_refs]
  known_outvars = [*outs_known, *residuals]
  known_effects = make_jaxpr_effects(jaxpr.constvars, ins_known_and_ref_res,
                                     known_outvars, known_eqns)

  # TODO(mattjj,necula): debug info should be updated here
  jaxpr_known = jaxpr.replace(
      invars=ins_known_and_ref_res, outvars=known_outvars,
      eqns=known_eqns, effects=known_effects,
      debug_info=jaxpr.debug_info.with_unknown_names())
  config.enable_checks.value and core.check_jaxpr(jaxpr_known)

  _, ins_staged = partition_list(in_inst, jaxpr.invars)
  _, outs_staged = partition_list(out_inst, jaxpr.outvars)
  staged_invars = [*residuals, *non_input_res_refs, *ins_staged]
  staged_effects = make_jaxpr_effects(jaxpr.constvars, staged_invars,
                                      outs_staged, staged_eqns)
  # TODO(mattjj,necula): debug info should be updated here
  jaxpr_staged = jaxpr.replace(
      invars=staged_invars, outvars=outs_staged, eqns=staged_eqns,
      effects=staged_effects,
      debug_info=jaxpr.debug_info.with_unknown_names())
  config.enable_checks.value and core.check_jaxpr(jaxpr_staged)

  return (jaxpr_known, jaxpr_staged, out_unknowns, out_inst, len(residuals),
          len(non_input_res_refs))

