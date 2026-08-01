
def python_policy_to_pyspiel_policy(python_tabular_policy):
  """Converts a TabularPolicy to a pyspiel.TabularPolicy."""
  infostates_to_probabilities = dict()
  for infostate, index in python_tabular_policy.state_lookup.items():
    probs = python_tabular_policy.action_probability_array[index]
    legals = python_tabular_policy.legal_actions_mask[index]

    action_probs = []
    for action, (prob, is_legal) in enumerate(zip(probs, legals)):
      if is_legal == 1:
        action_probs.append((action, prob))
    infostates_to_probabilities[infostate] = action_probs
  return pyspiel.TabularPolicy(infostates_to_probabilities)

