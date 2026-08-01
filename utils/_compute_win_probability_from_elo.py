
def _compute_win_probability_from_elo(rating_1, rating_2):
  """Computes the win probability of 1 vs 2 based on the provided Elo ratings.

  Args:
    rating_1: The Elo rating of player 1.
    rating_2: The Elo rating of player 2.

  Returns:
    The win probability of player 1, when playing against 2.
  """
  m = max(rating_1, rating_2)  # We subtract the max for numerical stability.

  m1 = 10**((rating_1 - m) / 400)
  m2 = 10**((rating_2 - m) / 400)

  return m1 / (m1 + m2)

