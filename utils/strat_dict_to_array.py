
def strat_dict_to_array(strategy_dictionary):
  """A helper function to convert the strategy dictionary mapping.

  Conversion applies action -> prob value to an array.

  Args:
    strategy_dictionary: a dictionary action -> prob value.

  Returns:
    strategy_array: an array with the ith action's value at the i-1th index.
  """
  actions = list(strategy_dictionary.keys())
  strategy_array = np.zeros((len(actions), 1))
  for action in range(len(actions)):
    strategy_array[action][0] = strategy_dictionary[actions[action]]
  return strategy_array

