
def _calc_nashconv(game, agent):
  """Calculates the NashConv of the current policy."""
  def _action_probabilities(state):
    probs = agent.action_probabilities(state)

    prob_dict = {}
    for a, m in enumerate(state.legal_actions_mask()):
      if m == 1:
        prob_dict[a] = probs[a]
    return prob_dict

  policy = open_spiel.python.policy.tabular_policy_from_callable(
      game, _action_probabilities
  )
  conv = open_spiel.python.algorithms.exploitability.nash_conv(game, policy)
  return conv

