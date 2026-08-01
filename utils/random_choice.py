
def random_choice(outcomes, probabilities):
  """Samples from discrete probability distribution.

  `numpy.choice` does not seem optimized for repeated calls, this code
  had higher performance.

  Args:
    outcomes: List of categorical outcomes.
    probabilities: Discrete probability distribtuion as list of floats.

  Returns:
    Entry of `outcomes` sampled according to the distribution.
  """
  cumsum = np.cumsum(probabilities)
  return outcomes[np.searchsorted(cumsum/cumsum[-1], random.random())]

