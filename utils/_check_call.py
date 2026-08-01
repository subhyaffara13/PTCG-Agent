
def _check_call(ctx_factory, prim, in_atoms, params):
  if "call_jaxpr" not in params:
    raise JaxprTypeError(
        f"Call primitive {prim} missing 'call_jaxpr' parameter")
  if isinstance(prim, ClosedCallPrimitive):
    call_jaxpr = params["call_jaxpr"].jaxpr
  else:
    call_jaxpr = params["call_jaxpr"]

  if len(in_atoms) != len(call_jaxpr.invars):
    raise JaxprTypeError(f"Call primitive {prim} with {len(in_atoms)} "
                         f"operands cannot call jaxpr with "
                         f"{len(call_jaxpr.invars)} inputs")

  # Check `call_jaxpr` can be applied to in_atoms.
  env: dict[Var, Atom | MutableTypecheckVal] = {}
  for v, x in zip(call_jaxpr.invars, in_atoms):
    if not typecompat(v.aval, x.aval):
      # TODO(mattjj): vars in error message are confusing b/c of Var.__repr__
      raise JaxprTypeError(f"Call primitive {prim} passes operand {x} of type "
                           f"{x.aval} to jaxpr expecting type "
                           f"{v.aval}")
    env[v] = x.val if type(x) is Literal else x

  check_jaxpr(call_jaxpr)

  out_avals = [x.aval for x in call_jaxpr.outvars]
  return out_avals, positional_effects(call_jaxpr)

