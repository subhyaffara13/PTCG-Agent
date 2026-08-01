
def max_support_two_player(variables):
  """Max support objective."""
  return cp.Minimize(cp.sum(variables['b_0']) + cp.sum(variables['b_1']))

