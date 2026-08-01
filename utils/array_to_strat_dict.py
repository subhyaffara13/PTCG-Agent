
def array_to_strat_dict(strategy_array, legal_actions):
  """A helper function to convert a strategy.

  Converts a strategy array to an action -> prob value dictionary.

  Args:
    strategy_array: an array with the ith action's value at the i-1th index.
    legal_actions: the list of all legal actions at the current state.

  Returns:
    strategy_dictionary: a dictionary action -> prob value.
  """
  return dict(zip(legal_actions, strategy_array))

