
def compute_counterfactual_values(infostate: InfostateNode) -> float:
  """Returns cfr value for an infostate.

  Args:
    infostate: Information state.

  Returns:
    Counterfactual value for infostate. This value is calculated from action
    value and policy of all legal actions of infostate information state.
  """
  if infostate.is_terminal():
    terminal_utility = 0
    for history_node in infostate.history_nodes:
      terminal_utility += history_node.reach_probs[
          0] * history_node.reach_probs[_get_opponent(
              infostate.player)] * history_node.world_state.get_utility(
                  infostate.player)
    return terminal_utility
  infostate_actions = infostate.get_actions()
  action_values = {action: 0 for action in infostate_actions}
  for action in infostate_actions:
    for child in infostate.children[action].values():
      action_values[action] += compute_counterfactual_values(child)
  infostate.counterfactual_action_values = action_values
  counterfactual_value = 0
  for action in infostate_actions:
    counterfactual_value += infostate.policy[action] * action_values[action]
  infostate.counterfactual_value = counterfactual_value
  return counterfactual_value

