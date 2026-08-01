
def return_cf_partial_sequence(num_actions, history, _):
  """Returns an array of all Counterfactual Partial Sequence deviations (CFPS).

  Returns an array of all Counterfactual Partial Sequence deviations (CFPS)
  with respect to an information set.

  Args:
    num_actions: the integer of all actions that can be taken at that
      information set.
    history: an array containing the prior actions played by the `player` to
      reach the information set.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent
    all CFPS deviations that are realizable at the information set.
  """
  prior_actions_in_memory = history
  memory_weights = [None]
  if history:
    memory_weights.append(np.ones(len(history)))
  for i in range(len(history)):
    possible_memory_weight = np.zeros(len(history))
    possible_memory_weight[0:i] = np.full(i, 1.0)
    memory_weights.append(possible_memory_weight)
  return return_all_non_identity_internal_deviations(
      num_actions, memory_weights, prior_actions_in_memory
  )

