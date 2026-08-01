
def jaxpr_const_args(jaxpr: Jaxpr) -> list[tuple[ArrayLike, AbstractValue]]:
  # The non-scalar constants in core.Literal, in the entire Jaxpr,
  # uniquified by id. These will be hoisted as const arguments to the functions
  # in which they appear.
  # See https://docs.jax.dev/en/latest/internals/constants.html
  if not config.use_simplified_jaxpr_constants.value:
    return []
  consts_by_id: dict[int, tuple[ArrayLike, AbstractValue]] = {}
  for v in jaxpr.outvars:
    if type(v) is Literal and is_hoistable(v):
      consts_by_id[id(v)] = (v.val, v.aval)

  for eqn in jaxpr.eqns:
    for v in eqn.invars:
      if type(v) is Literal and is_hoistable(v):
        consts_by_id[id(v)] = (v.val, v.aval)
    consts_by_id.update({id(v_aval[0]): v_aval
                         for v_aval in eqn_params_const_args(eqn.params)})
  return list(consts_by_id.values())

