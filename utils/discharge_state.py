
def discharge_state(
    closed_jaxpr: core.ClosedJaxpr,
    *,
    should_discharge: bool | Sequence[bool] = True,
    lower: bool = True,
) -> core.ClosedJaxpr:
  """Converts a stateful jaxpr into a pure one.

  Discharging replaces ``Ref`` inputs with regular values, threads updates
  through the computation, and returns updated ``Ref``s as additional outputs.

  Args:
    closed_jaxpr: A stateful jaxpr with ``Ref`` inputs.
    should_discharge: Whether to discharge each ``Ref`` input. If a single bool,
      applies to all inputs.
    lower: Whether to lower hijax to lojax while discharging.

  Returns:
    A pure jaxpr with no ``Read``/``Write``/``Accum`` effects. Discharged
    ``Ref`` inputs become regular value inputs, and their updated values are
    appended to the outputs.
  """
  if isinstance(should_discharge, bool):
    should_discharge = (should_discharge,) * len(closed_jaxpr.in_avals)
  return _discharge_state(closed_jaxpr, tuple(should_discharge), lower)


def discharge_state(
    jaxpr : core.Jaxpr,
    *,
    allow_additional_outputs: bool = True,
    dce: bool = False
) -> tuple[core.Jaxpr, list[bool], dict[int, int]]:
  """Converts a stateful fusion jaxpr into a pure one.

  Discharging replace ``Ref`` inputs with regular values and threads updates
  through the computation.

  Args:
    jaxpr: The fusion jaxpr to discharge.
    allow_additional_outputs: If True, the returned jaxpr will have an
      output for each modified Ref, containing the final, updated value for
      that Ref.
    dce: If True, perform dead code elimination on the discharged jaxpr,
      assuming all outputs are used.

  Returns:
    A tuple of ``(discharged_jaxpr, used_consts, output_input_aliases)`` where
    ``discharged_jaxpr`` is the discharged jaxpr, ``used_consts`` is a boolean
    list indicating which consts of the pre-DCE discharged jaxpr are
    used/included in the returned ``discharged_jaxpr`` (or all ``True`` if DCE
    was not requested), and ``output_input_aliases`` is a dict
    mapping ``outvars`` indices to ``constvars + inputvars`` indices in
    ``discharged_jaxpr` -- an entry ``(o, i)`` indicates that additional output
    ``o`` is the updated value for const/input ``i`` (which was a Ref in the
    original jaxpr).
  """
  should_discharge = [isinstance(v.aval, state_types.AbstractRef)
                      for v in itertools.chain(jaxpr.constvars, jaxpr.invars)]
  if not any(should_discharge):
    return jaxpr, [True] * len(jaxpr.constvars), {}

  jaxpr_no_consts = pe.convert_constvars_jaxpr(jaxpr)
  closed_discharged_jaxpr = state_discharge.discharge_state(
      core.ClosedJaxpr(jaxpr_no_consts, ()),
      should_discharge=should_discharge,
      lower=False,
  )
  assert not closed_discharged_jaxpr.consts, (
      closed_discharged_jaxpr.jaxpr, closed_discharged_jaxpr.consts)
  discharged_jaxpr = closed_discharged_jaxpr.jaxpr

  # ref_input_idxs[i] is the index, for the i-th new output, of the input Ref
  # that it corresponds to.
  ref_input_idxs = [i for i, v in enumerate(jaxpr_no_consts.invars)
              if isinstance(v.aval, state_types.AbstractRef)]
  num_new_outvars = len(discharged_jaxpr.outvars) - len(jaxpr.outvars)
  assert len(ref_input_idxs) == num_new_outvars, (
      len(ref_input_idxs), len(discharged_jaxpr.outvars), len(jaxpr.outvars),
  )

  # discharged_jaxpr has N new outputs, where N is the number of Ref inputs in
  # jaxpr_no_consts.  If allow_additional_outputs is True, we only want to keep
  # a new output if the original jaxpr actually writes to it.  If
  # allow_additional_outputs is False, we drop all of these new outputs.
  # (Callers will use this to discharge Ref updates to be outputs only for
  # output fusions.)
  write_idxs = get_write_indices(jaxpr) if allow_additional_outputs else set()
  keep_outvar = (
      [True] * len(jaxpr.outvars) + [i in write_idxs for i in ref_input_idxs])
  instantiate = ([i in write_idxs for i in range(len(jaxpr.constvars))]
                 + [True] * len(jaxpr.invars))
  if dce:
    discharged_jaxpr, used_inputs = pe.dce_jaxpr(
        discharged_jaxpr, used_outputs=keep_outvar, instantiate=instantiate)
    assert all(used_inputs[i] for i in write_idxs)
    used_consts = used_inputs[:len(jaxpr.constvars)]
  else:
    discharged_jaxpr = discharged_jaxpr.replace(
        outvars=[v for keep, v in zip(keep_outvar, discharged_jaxpr.outvars)
                 if keep])
    used_consts = [True] * len(jaxpr.constvars)
    used_inputs = used_consts + [True] * len(jaxpr.invars)
  discharged_jaxpr = pe.convert_invars_to_constvars(
      discharged_jaxpr, sum(used_consts))

  # adjust indices given used_inputs, so we can compute output_input_aliases
  new_input_idx = list(itertools.accumulate(used_inputs, initial=-1))[1:]
  write_idxs  = {new_input_idx[i] for i in write_idxs}
  ref_input_idxs = [new_input_idx[i] for i in ref_input_idxs if used_inputs[i]]
  written_ref_input_idxs = [i for i in ref_input_idxs if i in write_idxs]
  output_input_aliases = {(i + len(jaxpr.outvars)): j
                           for i, j in enumerate(written_ref_input_idxs)}
  assert len(output_input_aliases) == len(write_idxs), (
      ref_input_idxs, write_idxs, output_input_aliases
  )
  return discharged_jaxpr, used_consts, output_input_aliases

