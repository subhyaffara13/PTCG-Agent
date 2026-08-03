import itertools

def compute_payoff_epsilon(
    game: coalitional_game.CoalitionalGame,
    p: np.ndarray
) -> float:
  """For a payoff vector p, get max_e s.t. p dot c + e >= V(c).

  Warning! Enumerates all coalitions.

  Args:
    game: the game to enumerate.
    p: the payoff vector.

  Returns:
    the value max_e s.t. p dot c + e >= V(C) for all subsets C subseteq N.
  """
  epsilon = 0
  for c in itertools.product([0, 1], repeat=game.num_players()):
    coalition = np.asarray(c)
    val_c = game.coalition_values(coalition)
    payoffs_to_coalition = np.inner(p, coalition)
    epsilon = max(epsilon, val_c - payoffs_to_coalition)
  return epsilon

