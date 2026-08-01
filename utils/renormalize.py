
def renormalize(probabilities):
  """Replaces all negative entries with zeroes and normalizes the result.

  Args:
    probabilities: probability vector to renormalize. Has to be one-dimensional.

  Returns:
    Renormalized probabilities.
  """
  probabilities[probabilities < 0] = 0
  probabilities = probabilities / np.sum(probabilities)
  return probabilities

