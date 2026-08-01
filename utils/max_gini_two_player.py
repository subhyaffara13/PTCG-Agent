
def max_gini_two_player(variables):
  """Max gini objective."""
  return cp.Minimize(
      cp.sum(cp.square(variables['x_0'])) + cp.sum(cp.square(variables['x_1']))
  )

