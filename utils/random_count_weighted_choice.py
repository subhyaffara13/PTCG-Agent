
def random_count_weighted_choice(count_weight):
  """Returns a randomly sampled index i with P ~ 1 / (count_weight[i] + 1).

  Allows random sampling to prioritize indexes that haven't been sampled as many
  times as others.

  Args:
    count_weight: A list of counts to sample an index from.

  Returns:
    Randomly-sampled index.
  """
  indexes = list(range(len(count_weight)))
  p = np.array([1 / (weight + 1) for weight in count_weight])
  p /= np.sum(p)
  chosen_index = np.random.choice(indexes, p=p)
  return chosen_index

