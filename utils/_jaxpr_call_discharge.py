
def _jaxpr_call_discharge(
    flat_should_discharge,
    in_avals,
    out_avals,
    *flat_args,
    jaxpr,
    ref_treedefs,
    program_ids_treedef,
):
  del in_avals, out_avals  # Unused.
  flat_should_discharge = util.split_list(
      flat_should_discharge,
      [treedef.num_leaves for treedef in ref_treedefs[: len(ref_treedefs) - 1]],
  )
  should_discharge = [*map(any, flat_should_discharge)]
  discharged_closed_jaxpr = state_discharge.discharge_state(
      jax_core.ClosedJaxpr(jaxpr, ()), should_discharge=should_discharge
  )
  discharged_jaxpr, discharged_consts = discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts
  assert not discharged_consts
  outs = jaxpr_call_p.bind(
      *flat_args,
      jaxpr=discharged_jaxpr,
      ref_treedefs=tuple(ref_treedefs),
      program_ids_treedef=program_ids_treedef,
  )
  discharged_outs_it = iter(outs[len(jaxpr.outvars) :])
  new_in_vals = (
      tuple(
          itertools.chain.from_iterable(
              [next(discharged_outs_it) if discharged else None]
              * ref_treedefs[idx].num_leaves
              for idx, discharged in enumerate(should_discharge)
          )
      )
      + (None,) * program_ids_treedef.num_leaves
  )
  return new_in_vals, outs[: len(jaxpr.outvars)]

