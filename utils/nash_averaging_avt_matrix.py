
def nash_averaging_avt_matrix(s_mat, eps=0.0):
  """Apply the agent-vs-task Nash Averaging from Appendix D, from a matrix.

  Args:
    s_mat: The S matrix from the paper, representing m rows (agents) and n
      columns (tasks), with scores for the agent on the task. Note that the
      values need not be normalized, but will be normalized across tasks before
      being processed.
    eps: minimum probability threshold.

  Returns:
    maxent_nash: nash mixture for row player and column player
    nash_avg_score: the expected payoff under maxent_nash
  """
  m, n = s_mat.shape
  min_payoffs = np.min(s_mat, axis=0)
  max_payoffs = np.max(s_mat, axis=0)
  std_p_mat = (s_mat - min_payoffs) / (max_payoffs - min_payoffs)
  a_mat = np.block([
      [np.zeros(shape=(m, m)), std_p_mat],
      [-std_p_mat.T, np.zeros(shape=(n, n))],
  ])
  pa_sol, pe_sol = _max_entropy_symmetric_nash_avt(
      a_mat, num_agents=m, num_tasks=n, eps=eps)
  pa, pe = np.asarray(pa_sol), np.asarray(pe_sol)
  return (pa, pe), (std_p_mat.dot(pe), -std_p_mat.T.dot(pa))

