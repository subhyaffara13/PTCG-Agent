
def _eval_jaxpr_discharge_state(
    jaxpr: core.Jaxpr, should_discharge: Sequence[bool], consts: Sequence[Any],
    *args: Any):
  env = Environment({})

  foreach(env.write, jaxpr.constvars, consts)
  # Here some args may correspond to `Ref` avals but they'll be treated like
  # regular values in this interpreter.
  foreach(env.write, jaxpr.invars, args)

  refs_to_discharge = {id(v.aval) for v, d in zip(jaxpr.invars, should_discharge)
                       if d and isinstance(v.aval, AbstractRef)}

  for eqn in jaxpr.eqns:
    name_stack = source_info_util.current_name_stack() + eqn.source_info.name_stack
    traceback = eqn.source_info.traceback
    with source_info_util.user_context(
        traceback, name_stack=name_stack), eqn.ctx.manager:
      should_discharge = [id(v.aval) in refs_to_discharge for v in eqn.invars]
      if eqn.primitive is core.ref_p:
        [invar], [outvar] = eqn.invars, eqn.outvars
        ans = env.read(invar)
        if config.refs_to_pins.value:
          ans = pin(ans)
        refs_to_discharge.add(id(outvar.aval))
      elif eqn.primitive is core.empty_ref_p:
        [], [outvar] = eqn.invars, eqn.outvars
        assert isinstance(outvar.aval, AbstractRef)
        aval = outvar.aval.inner_aval
        if not isinstance(aval, core.ShapedArray):
          raise NotImplementedError  # TODO(sharadmv)
        ans = lax.empty(aval.shape, aval.dtype)
        refs_to_discharge.add(id(outvar.aval))
      elif eqn.primitive is core.free_ref_p:
        [invar], [] = eqn.invars, eqn.outvars
        refs_to_discharge.remove(id(invar.aval))
        ans = ()
      elif eqn.primitive is core.freeze_p:
        [invar], [outvar] = eqn.invars, eqn.outvars
        ans = env.read(invar)
        if config.refs_to_pins.value:
          ans = unpin(ans)
        refs_to_discharge.remove(id(invar.aval))
      elif any(should_discharge) or core.internal_mutable_array_effect in eqn.effects:
        if eqn.primitive in _partial_discharge_rules:
          rule: DischargeRule = partial(_partial_discharge_rules[eqn.primitive], should_discharge)
        elif eqn.primitive in _discharge_rules:
          rule = _discharge_rules[eqn.primitive]
        else:
          raise NotImplementedError(
              f"No state discharge rule implemented for primitive: {eqn.primitive}")
        invals = map(env.read, eqn.invars)
        in_avals = [v.aval for v in eqn.invars]
        out_avals = [v.aval for v in eqn.outvars]
        new_invals, ans = rule(
            in_avals, out_avals, *invals, **eqn.params)
        for invar, should, new_inval in zip(eqn.invars, should_discharge, new_invals):
          if new_inval is not None:
            if not should:
              raise ValueError(
                  f"Did not ask for inval to be discharged but it was. ({invar=},"
                  f" {new_inval=})"
              )
            env.write(invar, new_inval)  # pyrefly: ignore[bad-argument-type]
      else:
        # Default primitive rule, similar to `core.eval_jaxpr`. Note that here
        # we assume any higher-order primitives inside of the jaxpr are *not*
        # stateful.
        bind_params = eqn.primitive.get_bind_params(eqn.params)
        ans = eqn.primitive.bind(*map(env.read, eqn.invars), **bind_params)
    if eqn.primitive.multiple_results:
      foreach(env.write, eqn.outvars, ans)
    else:
      env.write(eqn.outvars[0], ans)
  # By convention, we return the outputs of the jaxpr first and then the final
  # values of the `Ref`s. Callers to this function should be able to split
  # them up by looking at `len(jaxpr.outvars)`.
  out_vals = map(env.read, jaxpr.outvars)
  ref_vals = map(
      env.read, [v for v in jaxpr.invars if id(v.aval) in refs_to_discharge])
  return [*out_vals, *ref_vals]

