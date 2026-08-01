
def compute_best_response_policy(infostate: InfostateNode) -> float:
  """Calculate best response policy and returns best response value of infostate.

  Args:
    infostate: Information state.

  Returns:
    Best response value similar to what compute_best_response_values returns.
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
      action_values[action] += compute_best_response_policy(child)

  infostate.policy = {action: 0 for action in infostate.get_actions()}
  max_action_value = max(action_values.values())
  for action in infostate_actions:
    if action_values[action] == max_action_value:
      infostate.policy[action] = 1
      break
  return max_action_value

