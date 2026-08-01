
def _alpha_beta(state, depth, alpha, beta, value_function,
                maximizing_player_id):
  """An alpha-beta algorithm.

  Implements a min-max algorithm with alpha-beta pruning.
  See for example https://en.wikipedia.org/wiki/Alpha-beta_pruning

  Arguments:
    state: The current state node of the game.
    depth: The maximum depth for the min/max search.
    alpha: best value that the MAX player can guarantee (if the value is <= than
      alpha, the MAX player will avoid it).
    beta: the best value that the MIN currently can guarantee (if the value is
      >= than beta, the MIN player will avoid it).
    value_function: An optional function mapping a Spiel `State` to a numerical
      value, to be used as the value of the maximizing player for a node when we
      reach `maximum_depth` and the node is not terminal.
    maximizing_player_id: The id of the MAX player. The other player is assumed
      to be MIN.

  Returns:
    A tuple of the optimal value of the sub-game starting in state
    (given alpha/beta) and the move that achieved it.

  Raises:
    NotImplementedError: If we reach the maximum depth. Given we have no value
      function for a non-terminal node, we cannot break early.
  """
  if state.is_terminal():
    return state.player_return(maximizing_player_id), None

  if depth == 0 and value_function is None:
    raise NotImplementedError(
        "We assume we can walk the full depth of the tree. "
        "Try increasing the maximum_depth or provide a value_function.")
  if depth == 0:
    return value_function(state), None

  player = state.current_player()
  best_action = -1
  if player == maximizing_player_id:
    value = -float("inf")
    for action in state.legal_actions():
      child_state = state.clone()
      child_state.apply_action(action)
      child_value, _ = _alpha_beta(child_state, depth - 1, alpha, beta,
                                   value_function, maximizing_player_id)
      if child_value > value:
        value = child_value
        best_action = action
      alpha = max(alpha, value)
      if alpha >= beta:
        break  # beta cut-off
    return value, best_action
  else:
    value = float("inf")
    for action in state.legal_actions():
      child_state = state.clone()
      child_state.apply_action(action)
      child_value, _ = _alpha_beta(child_state, depth - 1, alpha, beta,
                                   value_function, maximizing_player_id)
      if child_value < value:
        value = child_value
        best_action = action
      beta = min(beta, value)
      if alpha >= beta:
        break  # alpha cut-off
    return value, best_action

