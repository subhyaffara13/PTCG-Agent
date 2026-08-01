
def _move_outvars_to_back(jaxpr, to_move: tuple[bool, ...]) -> ClosedJaxpr:
  new_outvars = _move_to_front(jaxpr.jaxpr.outvars, map(op.not_, to_move))
  return ClosedJaxpr(jaxpr.jaxpr.replace(outvars=new_outvars), jaxpr.consts)

