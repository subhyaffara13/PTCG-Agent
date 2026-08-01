
def _move_binders_to_front(jaxpr: ClosedJaxpr, to_move: tuple[bool, ...]
                           ) -> ClosedJaxpr:
  assert len(jaxpr.in_avals) == len(to_move)
  constvars, invars = jaxpr.jaxpr.constvars, jaxpr.jaxpr.invars
  new_invars = _move_to_front(invars, to_move)
  if jaxpr.jaxpr.debug_info.arg_names is None:
    new_arg_names = None
  else:
    new_arg_names = tuple(_move_to_front(jaxpr.jaxpr.debug_info.arg_names, to_move))
  dbg = jaxpr.jaxpr.debug_info._replace(arg_names=new_arg_names)
  new_jaxpr = jaxpr.jaxpr.replace(
      constvars=constvars, invars=new_invars, debug_info=dbg)
  return ClosedJaxpr(new_jaxpr, jaxpr.consts)

