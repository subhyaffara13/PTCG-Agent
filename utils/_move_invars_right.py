
def _move_invars_right(jaxpr: ClosedJaxpr, to_move: tuple[bool, ...]):
  invars, rest = split_list(jaxpr.jaxpr.invars, [len(to_move)])
  left_invars, right_invars = partition_list(to_move, invars)
  new_invars = [*left_invars, *right_invars, *rest]
  new_jaxpr = jaxpr.jaxpr.replace(invars=new_invars)
  return jaxpr.replace(jaxpr=new_jaxpr)

