
def return_cs_partial_sequence_orginal(
    num_actions, history, prior_legal_actions
):
  """Returns an array of all Casual Partial Sequence deviations.

  Returns an array of all Casual Partial Sequence deviations with respect to
  an information set.

  Args:
    num_actions: the integer of all actions that can be taken at that
      information set
    history: an array containing the prior actions played by the `player` to
      reach the information set.
    prior_legal_actions: a 2d array containing the legal actions for each
      preceeding state.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent all
    Casual Partial Sequence deviations that are realizable at the
    information set.
  """
  prior_actions_in_memory = history
  external_memory_weights = []

  for i in range(len(history)):
    possible_memory_weight = np.zeros(len(history))
    possible_memory_weight[0:i] = np.full(i, 1.0)
    external_memory_weights.append(possible_memory_weight)

  external = return_all_external_modified_deviations(
      num_actions,
      external_memory_weights,
      prior_legal_actions,
      prior_actions_in_memory,
  )
  internal = return_informed_action(num_actions, history, None)

  cf_ext = return_informed_cf(num_actions, history, None)
  return np.concatenate((external, internal, cf_ext))

