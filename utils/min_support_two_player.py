
def min_support_two_player(variables):
  """Min support objective."""
  return cp.Maximize(cp.sum(variables['b_0']) + cp.sum(variables['b_1']))

