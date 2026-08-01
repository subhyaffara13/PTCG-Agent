
def return_identity_deviation(
    num_actions, possible_prior_weights, prior_memory_actions
):
  deviations = []
  for prior_actions_weight in possible_prior_weights:
    deviations.append(
        LocalDeviationWithTimeSelection(
            0, 0, num_actions, prior_actions_weight, prior_memory_actions, False
        )
    )
  return deviations

