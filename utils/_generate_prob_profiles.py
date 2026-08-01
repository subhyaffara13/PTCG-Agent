
def _generate_prob_profiles(num_items, num_slots):
  """Another implementation of `distribution` for test purposes.

  This function is the original implementation from Karl. jblespiau@ find it
  useful to add it here as: 1) an additional test of our function 2) a check
  that the initial code is correct too.

  Args:
    num_items: The number of items to distribute.
    num_slots: The number of slots.

  Returns:
    A numpy array of shape [num_distributions, num_slots].
  """
  if num_slots == 1:
    return np.array([num_items])

  num_rows = utils.n_choose_k(num_items + num_slots - 1, num_items)
  distributions = np.empty([num_rows, num_slots])

  ind = 0
  for i in range(0, num_items + 1):
    n_tmp = num_items - i
    k_tmp = num_slots - 1
    distributions_tmp = _generate_prob_profiles(n_tmp, k_tmp)
    distributions[ind:ind +
                  np.shape(distributions_tmp)[0], :] = np.column_stack(
                      (np.array((np.ones(np.shape(distributions_tmp)[0]) * i)),
                       distributions_tmp))
    ind = ind + np.shape(distributions_tmp)[0]

  return distributions

