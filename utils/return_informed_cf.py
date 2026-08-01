
def return_informed_cf(num_actions, history, _):
  """Returns an array of all Informed Counterfactual deviations.

  Returns an array of all Informed Counterfactual deviations with respect with
  respect to an information set.

  Args:
    num_actions: the integer of all actions that can be taken at that
      information set.
    history: an array containing the prior actions played by the `player` to
      reach the information set.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent all
    Informed CF deviations that are realizable at the information set.
  """
  memory_weights = [None]
  prior_actions_in_memory = np.zeros(len(history))
  return return_all_non_identity_internal_deviations(
      num_actions, memory_weights, prior_actions_in_memory
  )

