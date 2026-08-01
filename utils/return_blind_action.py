
def return_blind_action(num_actions, history, _):
  """Returns an array of all Blind Action deviations.

  Returns an array of all Blind Action deviations. with respect to an with
  respect to an information set.

  Args:
    num_actions: the integer of all actions that can be taken at that
      information set.
    history: an array containing the prior actions played by the `player` to
      reach the information set.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent all
    Blind Action deviations that are realizable at the information set.
  """
  memory_weights = [np.full(len(history), 1)]
  prior_actions_in_memory = history
  return return_all_external_deviations(
      num_actions, memory_weights, prior_actions_in_memory
  )

