
def _max_entropy_symmetric_nash(p_mat, eps=1e-9):
  """Solves for the maxent symmetric nash for symmetric 2P zero-sum games.

    Using convex programming:
      min p^Tlog(p)
      s.t.
      p_mat.dot(p) <= 0, since game value must be 0
      p >= 0
      1^T * p = 1

  Args:
    p_mat: an N*N anti-symmetric payoff matrix for the row player
    eps: minimum probability threshold

  Returns:
    p*: a maxent symmetric nash
  """
  assert np.array_equal(p_mat, -p_mat.T) and eps >= 0 and eps <= 0.5
  n = len(p_mat)
  x = cp.Variable(shape=n)
  obj = cp.Maximize(cp.sum(cp.entr(x)))
  constraints = [p_mat @ x <= 0, x >= eps * np.ones(n)]
  constraints.append(cp.sum(x) == 1)
  prob = cp.Problem(obj, constraints)
  prob.solve()
  return x.value.reshape((-1, 1))

