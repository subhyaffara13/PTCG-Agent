
def compute_best_response_values(infostate: InfostateNode) -> float:
  """Returns best response value for an infostate.

  Args:
    infostate: Information state.

  Returns:
    Best response value, which is the maximum action value chosen among all
    actions values of possible actions from infostate. If information state is a
    terminal node in the game tree, this value is calculated from history nodes
    reach probability for player and opponent, and game utility of terminal
    node. If infostate is not terminal, this value will be calculated in a
    recursive way.
  """
  if infostate.is_terminal():
    terminal_utility = 0
    for history_node in infostate.history_nodes:
      terminal_utility += history_node.reach_probs[
          0] * history_node.reach_probs[_get_opponent(
              infostate.player)] * history_node.world_state.get_utility(
                  infostate.player)
    return terminal_utility
  action_values = {action: 0 for action in infostate.get_actions()}
  infostate_actions = infostate.get_actions()
  for action in infostate_actions:
    action_values[action] = 0
    for child in infostate.children[action].values():
      action_values[action] += compute_best_response_values(child)
  return max(action_values.values())

