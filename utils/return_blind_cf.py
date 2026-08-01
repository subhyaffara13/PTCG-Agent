
def return_blind_cf(num_actions, history, _):
  """Returns an array of all Blind Counterfactual deviations.

  Returns an array of all Blind Counterfactual deviations with respect to an
  information set.

  Note: EFR using only Blind Counterfactual deviations is equivalent
  to vanilla Counterfactual Regret Minimisation (CFR).
  Args:
    num_actions: the integer of all actions that can be taken at that
      information set.
    history: an array containing the prior actions played by the `player` to
      reach the information set.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent all
    Blind CF deviations that are realizable at the information set.
  """
  memory_weights = [None]
  prior_actions_in_memory = np.zeros(len(history))
  return return_all_external_deviations(
      num_actions, memory_weights, prior_actions_in_memory
  )

