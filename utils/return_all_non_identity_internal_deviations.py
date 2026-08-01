
def return_all_non_identity_internal_deviations(
    num_actions, possible_prior_weights, prior_memory_actions
):
  """Returns all non-identity internal deviations."""
  deviations = []
  for prior_actions_weight in possible_prior_weights:
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
  return deviations

