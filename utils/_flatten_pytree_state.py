
def _flatten_pytree_state(state: PytreeState):
  return (), (state.initializing, state.is_setup)

