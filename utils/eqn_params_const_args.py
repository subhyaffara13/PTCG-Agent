
def eqn_params_const_args(params) -> list[tuple[ArrayLike, AbstractValue]]:
  consts_by_id: dict[int, tuple[ArrayLike, AbstractValue]] = {}
  for j in jaxprs_in_params(params):
    consts_by_id.update(
        {id(v_aval[0]): v_aval for v_aval in jaxpr_const_args(j)}
    )
  return list(consts_by_id.values())

