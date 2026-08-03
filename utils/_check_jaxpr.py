from typing import Callable

def _check_jaxpr(
    ctx_factory: Callable[[], tuple[JaxprPpContext, JaxprPpSettings]],
    jaxpr: Jaxpr
  ) -> None:
  env: dict[Var, Atom | MutableTypecheckVal] = {}

  def read(x: Atom) -> Atom | MutableTypecheckVal:
    # Check the type annotation is itself well-typed.
    check_type(ctx_factory, env, x.aval)
    if isinstance(x, Var):
      # Check the variable is in-scope and consistently typed.
      if x not in env:
        ctx, _ = ctx_factory()
        raise JaxprTypeError(f"Variable '{x.pretty_print(ctx)}' not defined")
      return env[x]
    elif isinstance(x, Literal):
      # Check that the literal matches its type annotation.
      if not typecheck(x.aval, x.val):
        ctx, _ = ctx_factory()
        raise JaxprTypeError(
            f"Literal value {x.val} does not match its type annotation "
            f"{pp_aval(x.aval, ctx)}")
      return x
    else:
      assert False, "syntactically invalid jaxpr"

  def write(v: Var, a: AvalQDD) -> None:
    aval, qdd = a.aval, a.qdd
    assert isinstance(v, Var), "syntactically invalid jaxpr"
    # Check the type annotation of the binder is itself well-typed.
    check_type(ctx_factory, env, v.aval)
    # Check that the variable is not already bound.
    if v in env:
      ctx, _ = ctx_factory()
      raise JaxprTypeError(f"Variable '{v.pretty_print(ctx)}' already bound")
    # Check that the computed type is consistent with the binder annotation.
    if not typematch(v.aval, aval):
      ctx, _ = ctx_factory()
      raise JaxprTypeError(
          f"Value for variable '{v.pretty_print(ctx)}' inconsistently typed "
          f"as {pp_aval(aval, ctx)} for let-binder of type {pp_aval(v.aval, ctx)}")

    # If the variable is not a DropVar, add it to the environment.
    if not isinstance(v, DropVar):
      if qdd is None:
        env[v] = v
      else:
        env[v] = MutableTypecheckVal(aval, MutableQuasiDynamicData(qdd))

  # # Don't return refs
  if config.mutable_array_checks.value:
    from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
    for v in jaxpr.outvars:
      if isinstance(v.aval, AbstractRef):
        raise JaxprTypeError("returned a ref!")

  # Check type annotations on lambda binders.
  for v in it.chain(jaxpr.constvars, jaxpr.invars):
    check_type(ctx_factory, env, v.aval)
    write(v, AvalQDD(v.aval, v.initial_qdd))

  # Check each eqn.
  input_vars = set(it.chain(jaxpr.constvars, jaxpr.invars))
  mut_arrays = set()
  for eqn_idx, eqn in enumerate(jaxpr.eqns):
    prim = eqn.primitive
    try:
      in_atoms = map(read, eqn.invars)
      in_avals = [AvalMutableQDD(x.aval, x.mutable_qdd) if isinstance(x, MutableTypecheckVal)
                  else x.aval for x in in_atoms]  # use in_atoms for dyn shapes

      # Compute the type of the primitive application.
      with eqn.ctx.manager:
        if prim in custom_typechecks:
          out_type, eqn_effects = custom_typechecks[prim](
            ctx_factory, *in_atoms, **eqn.params)
        elif prim.call_primitive:
          out_type, eqn_effects = _check_call(ctx_factory, prim, in_atoms,
                                              eqn.params)
        else:
          out_type, eqn_effects = check_eqn(prim, in_avals, eqn.params)

      # Check the computed effect type matches the eqn's annotation, and is
      # included in the jaxpr's annotation.
      if prim.ref_primitive:
        if prim.ref_allocating:
          outvar, = eqn.outvars
          mut_arrays.add(outvar)
      eqn_effects = resolve_input_effects(eqn_effects, eqn.invars)
      if eqn.effects != eqn_effects:
        raise JaxprTypeError("Inferred effects do not match equation effects. "
                             f"Equation effects: {eqn.effects}. "
                             f"Inferred effects: {eqn_effects}")
      for eff in eqn.effects:
        if isinstance(eff, effects.JaxprInputEffect):
          if eff.input in mut_arrays:
            continue
          if eff.input not in input_vars:
            raise JaxprTypeError(
                "Invalid `JaxprInputEffect`: must correspond to a jaxpr invar")
          if eff not in jaxpr.effects:
            raise JaxprTypeError(
                "Invalid `JaxprInputEffect`: must be present in jaxpr. "
                f"{eff} is not in {jaxpr.effects}.")
        elif isinstance(eff, NamedAxisEffect):
          # It is valid for a primitive to discharge the named axis effect.
          continue
        elif eff not in jaxpr.effects:
          raise JaxprTypeError("Equation effect not present in jaxpr effects. "
                               f"Equation effect: {eff}. "
                               f"Jaxpr effects: {jaxpr.effects}")

      # Check out_type matches the let-binders' annotation (after substitution).
      out_type = [t if isinstance(t, AvalQDD) else AvalQDD(t, None)
                  for t in out_type]
      foreach(write, eqn.outvars, out_type)

    except JaxprTypeError as e:
      ctx, settings = ctx_factory()
      msg, = e.args
      src = source_info_util.summarize(eqn.source_info)
      msg = "\n\n".join([msg, "in equation:", str(pp.nest(2, pp_eqn(eqn, ctx, settings))),
                         f"from source: {src}"])
      raise JaxprTypeError(msg, eqn_idx) from None

  # Check there are no output refs
  # TODO(mattjj): improve this error message
  if config.mutable_array_checks.value:
    from jax._src.state.types import AbstractRef  # pyrefly: ignore[missing-import]
    for v in jaxpr.outvars:
      if isinstance(v.aval, AbstractRef): raise TypeError("returned ref")

  # TODO(mattjj): include output type annotation on jaxpr and check it here
  foreach(read, jaxpr.outvars)

