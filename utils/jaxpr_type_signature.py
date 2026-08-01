
def jaxpr_type_signature(jaxpr: core.Jaxpr) -> KeyReuseSignature:
  """Parse the jaxpr to determine key reuse signature"""
  consumed: dict[core.Atom, bool | np.ndarray] = {}
  forwards: dict[core.Atom, core.Atom] = {}  # map forwarded outputs to inputs.

  def resolve_forwards(var: core.Atom) -> core.Atom:
    if not forwards:
      return var
    for _ in range(len(forwards) + 1):
      if isinstance(var, core.Literal):
        return var
      if var in forwards:
        var = forwards[var]
      else:
        return var
    raise ValueError("forwarding cycle detected")

  def is_key(var: core.Atom):
    return hasattr(var.aval, "dtype") and jax.dtypes.issubdtype(var.aval.dtype, jax.dtypes.prng_key)

  def sink(var: core.Atom, mask=True):
    if not is_key(var):
      return
    var = resolve_forwards(var)
    assert not isinstance(var, core.Literal)
    if np.any(np.logical_and(consumed.get(var, False), mask)):
      return True
    consumed[var] = np.logical_or(consumed.get(var, False), mask)

  def source(var: core.Atom, mask=False):
    if not is_key(var):
      return
    var = resolve_forwards(var)
    assert not isinstance(var, core.Literal)
    consumed[var] = mask

  def is_consumed(var: core.Atom):
    var = resolve_forwards(var)
    if isinstance(var, core.Literal):
      return False
    return consumed.get(var, False)

  for eqn in jaxpr.eqns:
    traceback = eqn.source_info.traceback
    name_stack = source_info_util.current_name_stack() + eqn.source_info.name_stack
    with source_info_util.user_context(traceback, name_stack=name_stack):
      signature = key_reuse_signature_from_eqn(eqn)
      if eqn.primitive == assert_consumed_value_p:
        # This is a special case that goes beyond normal key reuse logic.
        _check_consumed_value(eqn, is_consumed(eqn.invars[0]))

      for in_idx, out_idx in signature.forwards:
        forwards[eqn.outvars[out_idx]] = eqn.invars[in_idx]

      for snk in signature.sinks:
        if not 0 <= snk.idx < len(eqn.invars):
          raise KeyReuseError(f"In {eqn.primitive}, sink {snk.idx} out of range [0, {len(eqn.invars)}]")
        if sink(eqn.invars[snk.idx], snk.mask):
          raise KeyReuseError(f"In {eqn.primitive}, argument {snk.idx} is already consumed.")
      for var in eqn.outvars:
        if not isinstance(var, core.Literal) and var not in forwards:
          source(var, True)  # consumed unless in a Source.
      for src in signature.sources:
        if not 0 <= src.idx < len(eqn.outvars):
          raise KeyReuseError(f"In {eqn.primitive}, source {src.idx} out of range [0, {len(eqn.outvars)}]")
        source(eqn.outvars[src.idx])

  all_inputs: list[core.Atom] = [*jaxpr.invars, *jaxpr.constvars]
  return KeyReuseSignature(
    *(Sink(i, consumed[v]) for i, v in enumerate(all_inputs)
      if is_key(v) and np.any(consumed.get(v, False))),
    *(Source(i) for i, v in enumerate(jaxpr.outvars)
      if is_key(v) and resolve_forwards(v) not in all_inputs and not consumed.get(v, False)),
    *(Forward(all_inputs.index(resolve_forwards(outvar)), idx_out)
      for idx_out, outvar in enumerate(jaxpr.outvars)
      if is_key(outvar) and resolve_forwards(outvar) in all_inputs)
  )

