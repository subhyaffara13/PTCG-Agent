
def return_behavourial(num_actions, history, prior_legal_actions):
  """Returns an array of all single target behavioural deviations.

  The target behavioural deviations are with respect to an information set.

  Args:
    num_actions: the integer of all actions that can be taken at that
      information set
    history: an array containing the prior actions played by the `player` to
      reach the information set.
    prior_legal_actions: a 2d array containing the legal actions for each
      preceeding state.

  Returns:
    an array of LocalDeviationWithTimeSelection objects that represent
    all (single target) behaviourial deviations that are realizable at the
    information set.
  """
  deviations = []
  if not history:
    internal = return_all_non_identity_internal_deviations(
        num_actions, [None], history
    )
    for i in internal:
      deviations.append(i)
  else:
    for deviation_info in range(len(history)):
      prior_possible_memory_actions = generate_all_action_permutations(
          [], prior_legal_actions[: deviation_info + 1]
      )
      memory_weights = np.concatenate(
          (np.ones(deviation_info), np.zeros(len(history) - deviation_info))
      )
      for prior_memory_actions in prior_possible_memory_actions:
        prior_memory_actions = np.concatenate((
            prior_memory_actions,
            np.zeros(len(history) - len(prior_memory_actions)),
        ))
        for _ in range(len(history) - len(prior_memory_actions)):
          prior_memory_actions.append(0)
        prior_memory_actions_cp = prior_memory_actions.copy()
        internal = return_all_non_identity_internal_deviations(
            num_actions, [memory_weights], prior_memory_actions_cp
        )
        for i in internal:
          deviations.append(i)

  return deviations

