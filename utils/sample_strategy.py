
def sample_strategy(total_policies,
                    probabilities_of_playing_policies,
                    probs_are_marginal=True):
  """Samples strategies given probabilities.

  Uses independent sampling if probs_are_marginal, and joint sampling otherwise.

  Args:
    total_policies: if probs_are_marginal, this is a list, each element a list
      of each player's policies. If not, this is a list of joint policies. In
      both cases the policy orders must match that of
      probabilities_of_playing_policies.
    probabilities_of_playing_policies: if probs_are_marginal, this is a list,
      with the k-th element also a list specifying the play probabilities of the
      k-th player's policies. If not, this is a list of play probabilities of
      the joint policies specified by total_policies.
    probs_are_marginal: a boolean indicating if player-wise marginal
      probabilities are provided in probabilities_of_playing_policies. If False,
      then play_probabilities is assumed to specify joint distribution.

  Returns:
    sampled_policies: A list specifying a single sampled joint strategy.
  """

  if probs_are_marginal:
    return sample_strategy_marginal(total_policies,
                                    probabilities_of_playing_policies)
  else:
    return sample_strategy_joint(total_policies,
                                 probabilities_of_playing_policies)

