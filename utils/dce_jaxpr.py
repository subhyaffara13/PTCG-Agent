
def dce_jaxpr(jaxpr: Jaxpr, used_outputs: bool | Sequence[bool],
              instantiate: bool | Sequence[bool] = False,
              ) -> tuple[Jaxpr, list[bool]]:
  """Runs dead-code elementation on a given jaxpr.

  Args:
    jaxpr: The jaxpr to DCE.
    used_outputs: A list of bools indicating which outputs are used.
    instantiate: A bool or a list of bools indicating which inputs should be
      considered used, regardless of whether they are actually used in a jaxpr.
      If a bool, the same value is used for all inputs.

  Returns:
    A tuple of ``(new_jaxpr, used_inputs)``.
  """
  if type(used_outputs) is bool:
    used_outputs = (used_outputs,) * len(jaxpr.outvars)
  if type(instantiate) is bool:
    instantiate = (instantiate,) * len(jaxpr.invars)

  return _dce_jaxpr(jaxpr, tuple(used_outputs), tuple(instantiate))

