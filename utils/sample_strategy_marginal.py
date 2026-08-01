
def sample_strategy_marginal(total_policies, probabilities_of_playing_policies):
  """Samples strategies given marginal probabilities.

  Uses independent sampling if probs_are_marginal, and joint sampling otherwise.

  Args:
    total_policies: A list, each element a list of each player's policies.
    probabilities_of_playing_policies: This is a list, with the k-th element
      also a list specifying the play probabilities of the k-th player's
      policies.

  Returns:
    sampled_policies: A list specifying a single sampled joint strategy.
  """

  num_players = len(total_policies)
  sampled_policies = []
  for k in range(num_players):
    current_policies = total_policies[k]
    current_probabilities = probabilities_of_playing_policies[k]
    sampled_policy_k = random_choice(current_policies, current_probabilities)
    sampled_policies.append(sampled_policy_k)
  return sampled_policies

