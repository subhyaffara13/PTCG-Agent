
def _simplex_projection(updated_strategy, gamma=0.0):
  """Project updated_strategy on the closest point in L2-norm on gamma-simplex.

  Based on: https://eng.ucmerced.edu/people/wwang5/papers/SimplexProj.pdf

  Args:
    updated_strategy: New distribution value after being updated by update rule.
    gamma: minimal probability value when divided by number of actions.

  Returns:
    Projected distribution

  Algorithm description:
  It aims to find a scalar lam to be substracted by each dimension of v
  with the restriction that the resulted quantity should lie in [gamma, 1]
  until the resulted vector summed up to 1
  Example: [0.4, 0.7, 0.6], 0.2 -- > find lam=0.25
            --> [max(0.4-0.25, 0.2), max(0.7-0.25, 0.2), max(0.6-0.25, 0.2)]
            --> [0.2,  0.45, 0.35]
  """

  n = len(updated_strategy)
  idx = np.arange(1, n + 1)
  u = np.sort(updated_strategy)[::-1]
  u_tmp = (1 - np.cumsum(u) - (n - idx) * gamma) / idx
  rho = np.searchsorted(u + u_tmp <= gamma, True)
  return np.maximum(updated_strategy + u_tmp[rho - 1], gamma)

