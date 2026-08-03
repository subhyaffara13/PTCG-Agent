from typing import Any

def _run_state_impl(*args: Any, jaxpr: core.Jaxpr,
                    which_linear: tuple[bool, ...],
                    is_initialized: tuple[bool, ...]):
  del which_linear
  discharged_closed_jaxpr = discharge_state(core.ClosedJaxpr(jaxpr, ()))
  discharged_jaxpr, consts = discharged_closed_jaxpr.jaxpr, discharged_closed_jaxpr.consts
  # Initialize the args that are not initialized.
  args_it = iter(args)
  args = tuple(
      next(args_it) if is_init else _default_initialization(var.aval)
      for is_init, var in zip(is_initialized, discharged_jaxpr.invars)
  )
  return core.eval_jaxpr(discharged_jaxpr, consts, *args)

