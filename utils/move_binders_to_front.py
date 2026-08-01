
def move_binders_to_front(closed_jaxpr: ClosedJaxpr, to_move: Sequence[bool]
                          ) -> ClosedJaxpr:
  return _move_binders_to_front(closed_jaxpr, tuple(to_move))

