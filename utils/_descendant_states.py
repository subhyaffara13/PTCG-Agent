
def _descendant_states(
    state,
    depth_limit: int,
    depth: int,
    include_terminals: bool,
    include_chance_states: bool,
):
  """Recursive descendant state generator.

  Decision states are always yielded.

  Args:
    state: The current state.
    depth_limit: The descendant depth limit. Zero will ensure only
      `initial_state` is generated and negative numbers specify the absence of a
      limit.
    depth: The current descendant depth.
    include_terminals: Whether or not to include terminal states.
    include_chance_states: Whether or not to include chance states.

  Yields:
    `State`, a state that is `initial_state` or one of its descendants.
  """
  if state.is_terminal():
    if include_terminals:
      yield state
    return

  if depth > depth_limit >= 0:
    return

  if not state.is_chance_node() or include_chance_states:
    yield state

  for action in state.legal_actions():
    state_for_search = state.child(action)
    for substate in _descendant_states(
        state_for_search,
        depth_limit,
        depth + 1,
        include_terminals,
        include_chance_states,
    ):
      yield substate


def _descendant_states(
    state,
    depth_limit: int,
    depth: int,
    include_terminals: bool,
    include_chance_states: bool,
):
  """Recursive descendant state generator.

  Decision states are always yielded.

  Args:
    state: The current state.
    depth_limit: The descendant depth limit. Zero will ensure only
      `initial_state` is generated and negative numbers specify the absence of a
      limit.
    depth: The current descendant depth.
    include_terminals: Whether or not to include terminal states.
    include_chance_states: Whether or not to include chance states.

  Yields:
    `State`, a state that is `initial_state` or one of its descendants.
  """
  if state.is_terminal():
    if include_terminals:
      yield state
    return

  if depth > depth_limit >= 0:
    return

  if not state.is_chance_node() or include_chance_states:
    yield state

  for action in state.legal_actions():
    state_for_search = state.child(action)
    for substate in _descendant_states(
        state_for_search,
        depth_limit,
        depth + 1,
        include_terminals,
        include_chance_states,
    ):
      yield substate

