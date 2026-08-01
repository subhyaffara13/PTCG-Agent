
def kuhn_nash_equilibrium(alpha):
  """Returns a Nash Equilibrium in Kuhn parameterized by alpha in [0, 1/3].

  See https://en.wikipedia.org/wiki/Kuhn_poker#Optimal_strategy

  Args:
    alpha: The probability to bet on a Jack for Player 0.

  Raises:
    ValueError: If `alpha` is not within [0, 1/3].
  """
  if not 0 <= alpha <= 1 / 3:
    raise ValueError("alpha ({}) must be in [0, 1/3]".format(alpha))
  return pyspiel.kuhn_poker.get_optimal_policy(alpha)

