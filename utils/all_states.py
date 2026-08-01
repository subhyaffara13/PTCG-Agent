
def all_states(
    initial_state,
    depth_limit: int = -1,
    include_terminals: bool = False,
    include_chance_states: bool = False,
):
  """Generates states from `initial_state`.

  Generates the set of states that includes only the `initial_state` and its
  descendants that satisfy the inclusion criteria specified by the remaining
  parameters. Decision states are always included.

  Args:
    initial_state: The initial state from which to generate states.
    depth_limit: The descendant depth limit. Zero will ensure only
      `initial_state` is generated and negative numbers specify the absence of a
      limit. Defaults to no limit.
    include_terminals: Whether or not to include terminal states. Defaults to
      `False`.
    include_chance_states: Whether or not to include chance states. Defaults to
      `False`.

  Returns:
    A generator that yields the `initial_state` and its descendants that
    satisfy the inclusion criteria specified by the remaining parameters.
  """
  return _descendant_states(
      state=initial_state,
      depth_limit=depth_limit,
      depth=0,
      include_terminals=include_terminals,
      include_chance_states=include_chance_states,
  )


def all_states(
    initial_state,
    depth_limit: int = -1,
    include_terminals: bool = False,
    include_chance_states: bool = False,
):
  """Generates states from `initial_state`.

  Generates the set of states that includes only the `initial_state` and its
  descendants that satisfy the inclusion criteria specified by the remaining
  parameters. Decision states are always included.

  Args:
    initial_state: The initial state from which to generate states.
    depth_limit: The descendant depth limit. Zero will ensure only
      `initial_state` is generated and negative numbers specify the absence of a
      limit. Defaults to no limit.
    include_terminals: Whether or not to include terminal states. Defaults to
      `False`.
    include_chance_states: Whether or not to include chance states. Defaults to
      `False`.

  Returns:
    A generator that yields the `initial_state` and its descendants that
    satisfy the inclusion criteria specified by the remaining parameters.
  """
  return _descendant_states(
      state=initial_state,
      depth_limit=depth_limit,
      depth=0,
      include_terminals=include_terminals,
      include_chance_states=include_chance_states,
  )

