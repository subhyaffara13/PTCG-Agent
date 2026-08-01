
def _unflatten_pytree_state(static: tuple[bool, bool], _):
  initializing, setup = static
  return PytreeState(initializing, setup)

