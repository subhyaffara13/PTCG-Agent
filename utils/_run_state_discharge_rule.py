from typing import Any

def _run_state_discharge_rule(in_avals: Sequence[core.AbstractValue],
                              out_avals: Sequence[core.AbstractValue],
                              *args: Any, jaxpr: core.Jaxpr,
                              which_linear: Sequence[bool],
                              is_initialized: tuple[bool, ...]):
  if not all(is_initialized):
    raise NotImplementedError(
        "Uninitialized Refs are not supported in discharge."
    )
  del out_avals
  out_vals = run_state_p.bind(*args, jaxpr=jaxpr, which_linear=which_linear,
                              is_initialized=is_initialized)
  new_invals = []
  for aval, out_val in zip(in_avals, out_vals):
    new_invals.append(out_val if isinstance(aval, AbstractRef) else None)
  return new_invals, out_vals

