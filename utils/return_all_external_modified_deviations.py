
def return_all_external_modified_deviations(
    num_actions,
    possible_prior_weights,
    possible_prior_memory_actions,
    prior_memory_actions,
):
  """Returns all external deviations with modified memory actions."""
  deviations = []
  for prior_actions_weight in possible_prior_weights:
    try:
      modification_index = np.where(prior_actions_weight == 0)[0][0]
    except IndexError:
      modification_index = 0
    if modification_index == len(prior_memory_actions):
      for target in range(num_actions):
        deviations.append(
            LocalDeviationWithTimeSelection(
                target,
                target,
                num_actions,
                prior_actions_weight,
                prior_memory_actions,
                True,
            )
        )
    else:
      previous_action = prior_memory_actions[modification_index]
      for alt_action in possible_prior_memory_actions[modification_index]:
        prior_memory_actions[modification_index] = alt_action
        for target in range(num_actions):
          deviations.append(
              LocalDeviationWithTimeSelection(
                  target,
                  target,
                  num_actions,
                  prior_actions_weight,
                  prior_memory_actions.copy(),
                  True,
              )
          )
        prior_memory_actions[modification_index] = previous_action
  return deviations

