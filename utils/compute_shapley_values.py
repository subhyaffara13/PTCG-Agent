
def compute_shapley_values(
    game: coalitional_game.CoalitionalGame,
) -> np.ndarray:
  """Compute the Shapley values exactly.

  Uses Eq (2) of Mitchell et al. "Sampling Permutations for Shapley Value
  Estimation". https://people.math.sc.edu/cooper/shapley.pdf

  Args:
    game: the game to compute Shapley values for.

  Returns:
    shapley_values: a numpy array of Shapley values per player.
  """

  shapley_values_sum = np.zeros(game.num_players(), dtype=float)
  coalition = np.zeros(game.num_players(), dtype=int)
  empty_coalition_value = game.coalition_value(coalition)
  num_perms = 0
  for perm_tup in itertools.permutations(range(game.num_players())):
    perm = list(perm_tup)
    value_with = empty_coalition_value
    coalition.fill(0)
    for idx in range(game.num_players()):
      value_without = value_with  # re-use the one computed from the last iter
      i = perm[idx]
      coalition[i] = 1
      value_with = game.coalition_value(coalition)
      shapley_values_sum[i] += value_with - value_without
    num_perms += 1
  return shapley_values_sum / num_perms

