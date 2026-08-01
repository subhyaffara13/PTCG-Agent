
def move_outvars_to_back(jaxpr: ClosedJaxpr, to_move: Sequence[bool]) -> ClosedJaxpr:
  return _move_outvars_to_back(jaxpr, tuple(to_move))

