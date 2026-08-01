
def compute_approximate_shapley_values(
    game: coalitional_game.CoalitionalGame,
    num_samples: int,
) -> np.ndarray:
  """Compute the Shapley values using Monte Carlo estimation.

  Specifically, applies the implementation described in Section 2.3 of Mitchell
  et al. "Sampling Permutations for Shapley Value Estimation".
  https://people.math.sc.edu/cooper/shapley.pdf

  Args:
    game: the game to compute Shapley values for.
    num_samples: number of permutations to sample

  Returns:
    shapley_values: a numpy array of Shapley values per player.
  """

  shapley_values_sum = np.zeros(game.num_players(), dtype=float)
  coalition = np.zeros(game.num_players(), dtype=int)
  empty_coalition_value = game.coalition_value(coalition)
  for _ in range(num_samples):
    perm = np.random.permutation(game.num_players())
    value_with = empty_coalition_value
    coalition.fill(0)
    for idx in range(game.num_players()):
      value_without = value_with  # re-use the one computed from the last iter
      i = perm[idx]
      coalition[i] = 1
      value_with = game.coalition_value(coalition)
      shapley_values_sum[i] += value_with - value_without
  return shapley_values_sum / num_samples

