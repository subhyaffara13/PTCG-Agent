
def _action_probabilities(agent, state):
  probs = agent.action_probabilities(state)

  prob_dict = {}
  for a, m in enumerate(state.legal_actions_mask()):
    if m == 1:
      prob_dict[a] = probs[a]
  return prob_dict

