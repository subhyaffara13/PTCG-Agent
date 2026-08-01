
def _run_scoped_discharge_rule(
    should_discharge,
    in_avals,
    out_avals,
    *args_flat,
    jaxpr,
    collective_axes,
    ref_transforms,
    **_):
  del out_avals
  if collective_axes:
    raise NotImplementedError(
        "run_scoped discharge does not support collective_axes yet."
    )
  num_consts = len(args_flat)
  # discharge_state only discharges invars, not consts, so in order to
  # discharge the requested refs we need to move them to the invar set.
  jaxpr_noconst = pe.convert_constvars_jaxpr(jaxpr)
  num_return_values = len(jaxpr_noconst.outvars)
  discharged_closed_body = state_discharge.discharge_state(
      jax_core.ClosedJaxpr(jaxpr_noconst, ()),
      should_discharge=should_discharge + [False] * len(jaxpr.invars),
  )
  discharged_body, new_consts = discharged_closed_body.jaxpr, discharged_closed_body.consts
  if new_consts:
    raise NotImplementedError(
        "Cannot handle new consts created by state discharge.")

  # Lowering expects that the jaxpr.consts to be the eqn.invals.
  discharged_body = pe.convert_invars_to_constvars(discharged_body, num_consts)

  # Run_scoped discharged the external variables but the scoped ones
  # are not discharged.
  out = run_scoped_p.bind(
      *args_flat, jaxpr=discharged_body, collective_axes=collective_axes,
      ref_transforms=ref_transforms,
  )
  # Order of outputs:
  # (1) return values, (2) closed refs, (3) scoped refs.
  return_values = out[:num_return_values]
  ref_outputs = out[num_return_values:]
  # We update all ref values with their updated values from the discharged
  # body. For other values we leave them in place.
  updates = [
      ref_outputs.pop(0) if should and isinstance(aval, state.AbstractRef)
      else None for should, aval in zip(should_discharge, in_avals)]
  assert len(updates) == len(in_avals), f'{len(updates)} != {len(in_avals)}'
  return updates, return_values

