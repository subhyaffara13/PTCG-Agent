
def return_all_internal_modified_deviations(
    num_actions,
    possible_prior_weights,
    possible_prior_memory_actions,
    prior_memory_actions,
):
  """Returns all internal deviations with modified memory actions."""
  deviations = []
  for prior_actions_weight in possible_prior_weights:
    try:
      modification_index = np.where(prior_actions_weight == 0)[0][0]
    except IndexError:
      modification_index = 0
    if modification_index == len(prior_memory_actions):
      for target in range(num_actions):
        for source in range(num_actions):
          if source != target:
            deviations.append(
                LocalDeviationWithTimeSelection(
                    target,
                    source,
                    num_actions,
                    prior_actions_weight,
                    prior_memory_actions,
                    False,
                )
            )
    else:
      previous_action = prior_memory_actions[modification_index]
      for alt_action in possible_prior_memory_actions[modification_index]:
        prior_memory_actions[modification_index] = alt_action
        for target in range(num_actions):
          for source in range(num_actions):
            if source != target:
              deviations.append(
                  LocalDeviationWithTimeSelection(
                      target,
                      source,
                      num_actions,
                      prior_actions_weight,
                      prior_memory_actions.copy(),
                      False,
                  )
              )
        prior_memory_actions[modification_index] = previous_action
  return deviations

