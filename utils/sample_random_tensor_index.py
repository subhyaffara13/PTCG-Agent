
def sample_random_tensor_index(probabilities_of_index_tensor):
  shape = probabilities_of_index_tensor.shape
  reshaped_probas = probabilities_of_index_tensor.reshape(-1)

  strat_list = list(range(len(reshaped_probas)))
  chosen_index = random_choice(strat_list, reshaped_probas)
  return np.unravel_index(chosen_index, shape)

