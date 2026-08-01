
def _check_distribution_sum(distribution: DistributionDict, expected_sum: int):
  """Sanity check that the distribution sums to a given value."""
  sum_state_probabilities = sum(distribution.values())
  assert abs(sum_state_probabilities - expected_sum) < 1e-4, (
      "Sum of probabilities of all possible states should be the number of "
      f"population, it is {sum_state_probabilities}.")

