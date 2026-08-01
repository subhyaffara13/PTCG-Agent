
def dce_jaxpr_consts(jaxpr: Jaxpr, used_outputs: Sequence[bool],
                     instantiate: bool | Sequence[bool] = False,
                     ) -> tuple[Jaxpr, list[bool], list[bool]]:
  jaxpr_ = convert_constvars_jaxpr(jaxpr)
  new_jaxpr, used_inputs_ = dce_jaxpr(jaxpr_, used_outputs, instantiate)
  used_consts, used_inputs = split_list(used_inputs_, [len(jaxpr.constvars)])
  if sum(used_consts):
    new_jaxpr = convert_invars_to_constvars(new_jaxpr, sum(used_consts))
  return new_jaxpr, used_consts, used_inputs

