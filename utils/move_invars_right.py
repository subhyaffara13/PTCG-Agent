
def move_invars_right(jaxpr: ClosedJaxpr, to_move: Sequence[bool]):
  return _move_invars_right(jaxpr, tuple(to_move))

