
def assert_probabilities(array):
  if not all([item >= 0 for item in array]):
    raise ValueError("The vector must have all elements >= 0 items, not"
                     "{}".format(array))
  sum_ = np.sum(array)
  if not np.isclose(1, sum_):
    raise ValueError(
        "The sum of the probabilities  must be 1, not {}".format(sum_))

