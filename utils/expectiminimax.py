
def expectiminimax(state, depth, value_function, maximizing_player_id):
  """Runs expectiminimax until the specified depth.

  See https://en.wikipedia.org/wiki/Expectiminimax for details.

  Arguments:
    state: The state to start the search from.
    depth: The depth of the search (not counting chance nodes).
    value_function: A value function, taking in a state and returning a value,
      in terms of the maximizing_player_id.
    maximizing_player_id: The player running the search (current player at root
      of the search tree).

  Returns:
    A tuple (value, best_action) representing the value to the maximizing player
    and the best action that achieves that value. None is returned as the best
    action at chance nodes, the depth limit, and terminals.
  """
  if state.is_terminal():
    return state.player_return(maximizing_player_id), None

  if depth == 0:
    return value_function(state), None

  if state.is_chance_node():
    value = 0
    for outcome, prob in state.chance_outcomes():
      child_state = state.clone()
      child_state.apply_action(outcome)
      child_value, _ = expectiminimax(child_state, depth, value_function,
                                      maximizing_player_id)
      value += prob * child_value
    return value, None
  elif state.current_player() == maximizing_player_id:
    value = -float("inf")
    for action in state.legal_actions():
      child_state = state.clone()
      child_state.apply_action(action)
      child_value, _ = expectiminimax(child_state, depth - 1, value_function,
                                      maximizing_player_id)
      if child_value > value:
        value = child_value
        best_action = action
    return value, best_action
  else:
    value = float("inf")
    for action in state.legal_actions():
      child_state = state.clone()
      child_state.apply_action(action)
      child_value, _ = expectiminimax(child_state, depth - 1, value_function,
                                      maximizing_player_id)
      if child_value < value:
        value = child_value
        best_action = action
    return value, best_action

