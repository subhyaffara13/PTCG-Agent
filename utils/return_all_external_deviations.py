
def return_all_external_deviations(
    num_actions, possible_prior_weights, prior_memory_actions
):
  """Returns all external deviations."""
  deviations = []
  for prior_actions_weight in possible_prior_weights:
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
  return deviations

