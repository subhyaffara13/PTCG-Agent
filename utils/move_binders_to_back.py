
def move_binders_to_back(closed_jaxpr: ClosedJaxpr, to_move: Sequence[bool]
                         ) -> ClosedJaxpr:
  assert len(to_move) <= len(closed_jaxpr.invars)
  to_move = [*to_move] + [False] * (len(closed_jaxpr.invars) - len(to_move))
  return move_binders_to_front(closed_jaxpr, map(op.not_, to_move))

