
def nash_averaging(game, eps=0.0, a_v_a=True):
  """Nash averaging, see https://arxiv.org/abs/1806.02643.

  Args:
    game: a pyspiel game
    eps: minimum probability mass for maxent nash
    a_v_a: whether it is Agent-vs-Agent or Agent-vs-Task

  Returns:
    maxent_nash: nash mixture for row player and column player
    nash_avg_score: the expected payoff under maxent_nash
  """

  p_mat = game_payoffs_array(game)
  if len(p_mat) != 2:
    raise ValueError("Nash Averaging works only for two players.")
  if np.max(np.abs(p_mat[0] + p_mat[1])) > 0:
    raise ValueError("Must be zero-sum")
  if a_v_a:
    if not np.array_equal(p_mat[0], -p_mat[0].T):
      raise ValueError(
          "AvA only works for symmetric two-player zero-sum games.")
    maxent_nash = np.array(_max_entropy_symmetric_nash(p_mat[0], eps=eps))
    return maxent_nash, p_mat[0].dot(maxent_nash)

  # For AvT, see appendix D of the paper.
  # Here assumes the row player represents agents and the column player
  # represents tasks.
  # game does not have to be symmetric
  return nash_averaging_avt_matrix(p_mat[0], eps=eps)

